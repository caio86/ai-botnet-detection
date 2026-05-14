FROM iwaseyusuke/mininet:latest

WORKDIR /workspace

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  argus-server \
  argus-client \
  tcpdump \
  && rm -rf /var/lib/apt/lists/*

COPY ./botnet_topo.py .
COPY argus-conf/argus.conf .
COPY argus-conf/ra.conf .
COPY argus.sh .
COPY ../tungx3-random-forest.pkl .

CMD ["python3", "botnet_topo"]
