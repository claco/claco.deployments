FROM hashicorp/vault:latest

COPY config.hcl /vault/config/server.hcl

HEALTHCHECK --interval=5s --timeout=1s --start-period=3s --retries=3 CMD [ "nc", "-zv", "127.0.0.1", "8200" ]

CMD [ "vault", "server", "--config=/vault/config" ]
