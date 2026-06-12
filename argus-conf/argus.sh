(while true; do 
  # 1. O tcpdump captura o tráfego por 5 segundos e salva no pcap
  timeout 5 tcpdump -i s1-eth8 -w /tmp/lote_atual.pcap 2>/dev/null
  
  # 2. O Argus lê esse arquivo estático perfeitamente e o 'ra' converte para CSV
  if [ -s /tmp/lote_atual.pcap ]; then
      argus -r /tmp/lote_atual.pcap -w - | ra -r - -n -F argus/ra.conf -Z b
  fi
done) | python3 tungx3.py
