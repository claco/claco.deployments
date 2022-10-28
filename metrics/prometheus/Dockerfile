FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/prometheus.yml

HEALTHCHECK --interval=5s --timeout=1s --start-period=3s --retries=3 CMD [ "nc", "-zv", "127.0.0.1", "9090" ]
