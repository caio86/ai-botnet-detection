import sys
import pandas as pd
import joblib
import warnings

# Suppress pandas warnings to keep your terminal output clean
warnings.filterwarnings("ignore")

# --- 1. CONFIGURATION ---
MODEL_PATH = "tungx3-random-forest.pkl"  # Update with your exact path
BATCH_SIZE = 10  # Predict every 10 flows (Adjust for performance vs latency)

print("[*] Loading AI Model...", file=sys.stderr)
try:
    model = joblib.load(MODEL_PATH)
    expected_features = model.feature_names_in_
    print(f"Features esperadas pelo modelo: {expected_features}")
    print("[+] Model loaded successfully. Waiting for Argus data...", file=sys.stderr)
except Exception as e:
    print(f"[!] Error loading model: {e}", file=sys.stderr)
    sys.exit(1)


# --- 2. PREPROCESSING HELPERS ---
def clean_port(value):
    val_str = str(value).strip().lower()
    if val_str.startswith("0x"):
        return int(val_str, 16)
    try:
        return float(val_str)
    except ValueError:
        return -1


def categorize_port(port):
    if pd.isna(port) or port < 0:
        return 0
    elif 0 <= port <= 1023:
        return 1
    elif 1024 <= port <= 49151:
        return 2
    elif port >= 49152:
        return 3
    else:
        return 0


# --- 3. REAL-TIME LISTENING LOOP ---
headers = None
flow_batch = []

# Read line-by-line from the pipeline
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # print(line)
    # continue

    # Identify and save the header row
    if headers is None:
        if "stime" in line.lower() or "StartTime" in line:
            headers = [h.strip() for h in line.split(",")]
        continue

    # Skip any repeated headers from Argus
    if "stime" in line.lower():
        continue

    # CORREÇÃO 1: Tratar anomalias no tamanho da linha (ex: 13 colunas em vez de 12)
    linha_separada = line.split(",")

    # Se o Argus mandou colunas a mais (ex: vírgula sobrando no final), nós cortamos
    if len(linha_separada) > len(headers):
        linha_separada = linha_separada[: len(headers)]
    # Se o Argus mandou colunas a menos, preenchemos com vazio para o Pandas não quebrar
    elif len(linha_separada) < len(headers):
        linha_separada.extend([""] * (len(headers) - len(linha_separada)))

    flow_batch.append(linha_separada)

    # Once we hit our batch limit, process the data
    if len(flow_batch) >= BATCH_SIZE:
        # 1. Convert to DataFrame (Agora seguro contra erros de tamanho)
        df = pd.DataFrame(flow_batch, columns=headers)
        df_alert_context = df.copy()  # Keep raw data for logging

        df.drop(columns=['sTos', 'dTos', 'State'], inplace=True)
        df.drop(columns=['Label', 'StartTime', 'SrcAddr', 'DstAddr'], inplace=True)
        df = pd.get_dummies(df, columns=['Proto', 'Dir'])

        df['Sport'] = df['Sport'].apply(clean_port)
        df['Sport'] = df['Sport'].apply(categorize_port)
        df['Dport'] = df['Dport'].apply(clean_port)
        df['Dport'] = df['Dport'].apply(categorize_port)        

        df = df.reindex(columns=expected_features, fill_value=0)

        # 7. EXECUTE INFERENCE
        try:
            predictions = model.predict(df)

            # CORREÇÃO 3: Mover as variáveis para fora do IF para evitar NameError
            # 8. Alert on Detection
            for i, pred in enumerate(predictions):
                src = df_alert_context.iloc[i].get("SrcAddr", "Unknown")
                dst = df_alert_context.iloc[i].get("DstAddr", "Unknown")
                proto = df_alert_context.iloc[i].get("Proto", "Unknown")

                if pred == 1:
                    print(
                        f"[🚨 BOTNET DETECTED] Source: {src} | Destination: {dst} | Protocol: {proto}"
                    )
                else:
                    print(
                        f"[NORMAL TRAFFIC] Source: {src} | Destination: {dst} | Protocol: {proto}"
                    )
        except Exception as e:
            print(f"[!] Inference error on batch: {e}", file=sys.stderr)

        # Reset batch for the next flows
        flow_batch = []
