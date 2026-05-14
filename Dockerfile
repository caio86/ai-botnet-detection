FROM iwaseyusuke/mininet:latest

WORKDIR /workspace

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tcpdump tcpreplay argus-server argus-client python3-pip && \
  pip3 install numpy pandas matplotlib seaborn joblib imbalanced-learn scikit-learn
# && rm -rf /var/lib/apt/lists/*

COPY ./botnet_topo.py .

COPY ./tungx3-random-forest.pkl .
COPY ./tungx3.py .

# COPY argus-conf/argus.conf .
# COPY argus-conf/ra.conf .
# COPY argus-conf/argus.sh .
# COPY scripts-tcpreplay/bot1-victim.sh .

COPY pcaps/botnet-fast-flux-5-46-tratado.pcap pcaps/
COPY pcaps/botnet-rbot-3-44-tratado.pcap pcaps/

CMD ["python3", "botnet_topo"]
