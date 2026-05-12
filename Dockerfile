FROM iwaseyusuke/mininet:latest

WORKDIR /workspace

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  argus-server \
  argus-client \
  tcpdump \
  && rm -rf /var/lib/apt/lists/*

COPY ./botnet_topo.py .

CMD ["python3", "botnet_topo"]
