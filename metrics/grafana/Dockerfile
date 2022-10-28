FROM grafana/grafana-enterprise:latest

COPY custom.ini /etc/grafana/grafana.ini
COPY datasources.yml /etc/grafana/provisioning/datasources/prometheus.yml

HEALTHCHECK --interval=5s --timeout=1s --start-period=3s --retries=3 CMD [ "nc", "-zv", "127.0.0.1", "3000" ]
