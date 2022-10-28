FROM hashicorp/vault:latest

ARG VAULT_SECRETS_DIR="/vault/secrets"
ENV VAULT_SECRETS_DIR="${VAULT_SECRETS_DIR}"

RUN mkdir -p "${VAULT_SECRETS_DIR}" && chown vault:vault "${VAULT_SECRETS_DIR}"

RUN apk --no-cache add jq

COPY docker-entrypoint.sh /usr/local/bin/init.sh
COPY config.hcl /vault/config/proxy.hcl
COPY policies /vault/config/policies

VOLUME "${VAULT_SECRETS_DIR}"

HEALTHCHECK --interval=5s --timeout=1s --start-period=3s --retries=3 CMD [ "nc", "-zv", "127.0.0.1", "8200" ]

CMD [ "sh", "/usr/local/bin/init.sh" ]
