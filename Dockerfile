FROM iwaseyusuke/mininet:latest

WORKDIR /workspace

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tcpdump argus-server argus-client python3-pip && \
  pip3 install numpy pandas matplotlib seaborn joblib imbalanced-learn scikit-learn
# && rm -rf /var/lib/apt/lists/*

COPY ./botnet_topo.py .
COPY ./tungx3.py .
COPY ./argus-conf/argus.conf .
COPY ./argus-conf/ra.conf .
COPY ./argus-conf/argus.sh .
COPY ./tungx3-random-forest.pkl .

CMD ["python3", "botnet_topo"]
