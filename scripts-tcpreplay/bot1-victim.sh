#h1 tcpreplay-edit --endpoints=10.0.0.11:10.0.0.100 --enet-smac=00:00:00:00:00:11 --enet-dmac=00:00:00:00:00:99 --fixcsum -i bot1-eth0 botnet-capture-20110815-rbot-5-46.pcap
# tcprewrite --endpoints=10.0.0.11:10.0.0.100 --infile=botnet-rbot-5-46.pcap --outfile=botnet-rbot-5-46-tratado.pcap --fixcsum

argus -i s1-eth8 -w - | ra -r - -c , -s stime,dur,proto,saddr,sport,dir,daddr,dport,sate,stos,dtos,pkts,bytes,sbytes | python3 tungx3.py

### 5-46
bittwiste -I botnet-fast-flux-5-46.pcap -O botnet-fast-flux-5-46-temp.pcap -T ip -s 10.0.0.11 -d 10.0.0.100
bittwiste -I botnet-fast-flux-5-46-temp.pcap -O botnet-fast-flux-5-46-tratado.pcap -T eth -s 00:00:00:00:00:11 -d 00:00:00:00:00:99
rm botnet-fast-flux-5-46-temp.pcap

bot1 tcpreplay -i bot1-eth0 pcaps/botnet-fast-flux-5-46-tratado.pcap

### 3-44
bittwiste -I botnet-rbot-3-44.pcap -O botnet-rbot-3-44-temp.pcap -T ip -s 10.0.0.11 -d 10.0.0.100
bittwiste -I botnet-rbot-3-44-temp.pcap -O botnet-rbot-3-44-tratado.pcap -T eth -s 00:00:00:00:00:11 -d 00:00:00:00:00:99
rm botnet-rbot-3-44-temp.pcap

bot1 tcpreplay -i bot1-eth0 pcaps/botnet-rbot-3-44-tratado.pcap