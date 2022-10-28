#!/usr/bin/dumb-init /bin/sh
# shellcheck shell=sh

set -e

VAULT_HOME_DIR="${VAULT_HOME_DIR:-/home/vault}"
VAULT_POLICIES_DIR="${VAULT_POLICIES_DIR:-/vault/config/policies}"

# initialize vault if we haven't done so yet and put keys in root user
cd /root

if [ ! -f "init.json" ]; then
    vault operator init --format=json > init.json

    if [ ! -f ".vault-token" ]; then
        jq -r '.root_token' init.json > .vault-token
    fi
fi

# unseal vault if it is currently sealed
vault status --format=json > status.json || error_code=$?

if [ "${error_code}" -eq 2 ]; then
    vault operator unseal "$(jq -r '.unseal_keys_b64[0]' init.json)" > /dev/null
    vault operator unseal "$(jq -r '.unseal_keys_b64[1]' init.json)" > /dev/null
    vault operator unseal "$(jq -r '.unseal_keys_b64[2]' init.json)" > /dev/null
fi

# login to vault with the root token and configure backends
vault login --format=json - < .vault-token > login.json

# change ot the vault user home directory
cd ${VAULT_HOME_DIR}

vault auth enable approle > /dev/null
vault secrets enable --version=2 --path=casc kv > /dev/null

# configure casc (configuration as code) approle access
CASC_SECRETS_DIR="${CASC_SECRETS_DIR:-/vault/secrets/casc}"
CASC_APPROLE_NAME="${CASC_APPROLE_NAME:-casc}"

if [ ! -d "${CASC_SECRETS_DIR}" ]; then
    mkdir -p ${CASC_SECRETS_DIR}

    vault policy write casc-policy ${VAULT_POLICIES_DIR}/casc-policy.hcl > /dev/null
    vault write --force auth/approle/role/${CASC_APPROLE_NAME} token_policies="default,casc-policy" > /dev/null
    vault read --format=json auth/approle/role/${CASC_APPROLE_NAME}/role-id | jq -r '.data.role_id' > ${CASC_SECRETS_DIR}/role-id
    vault write --format=json --force auth/approle/role/${CASC_APPROLE_NAME}/secret-id | jq -r '.data.secret_id' > ${CASC_SECRETS_DIR}/secret-id
    vault write --format=json auth/approle/login role_id="$(cat ${CASC_SECRETS_DIR}/role-id)" secret_id="$(cat ${CASC_SECRETS_DIR}/secret-id)" | jq -r '.auth.client_token' > ${CASC_SECRETS_DIR}/.vault-token

    vault kv put --mount=casc jenkins \
        username="$(cat /run/secrets/username)" password="$(cat /run/secrets/password)" \
        role_id="$(cat ${CASC_SECRETS_DIR}/role-id)" secret_id="$(cat ${CASC_SECRETS_DIR}/secret-id)" \
        id_rsa="$(cat /run/secrets/id_rsa)" id_rsa.pub="$(cat /run/secrets/id_rsa.pub)" \
        --format=json > /root/${CASC_APPROLE_NAME}-secrets.json

    # link the approle auto-auth credentials for the proxy service/user
    ln -s ${CASC_SECRETS_DIR}/role-id ${VAULT_HOME_DIR}/role-id
    ln -s ${CASC_SECRETS_DIR}/secret-id ${VAULT_HOME_DIR}/secret-id
fi

# configure jenkins (pipeline plugin) approle access
JENKINS_SECRETS_DIR="${JENKINS_SECRETS_DIR:-/vault/secrets/jenkins}"
JENKINS_APPROLE_NAME="${JENKINS_APPROLE_NAME:-jenkins}"

if [ ! -d "${JENKINS_SECRETS_DIR}" ]; then
    mkdir -p ${JENKINS_SECRETS_DIR}

    vault policy write jenkins-policy ${VAULT_POLICIES_DIR}/jenkins-policy.hcl > /dev/null
    vault write --force auth/approle/role/${JENKINS_APPROLE_NAME} token_policies="default,jenkins-policy" > /dev/null
    vault read --format=json auth/approle/role/${JENKINS_APPROLE_NAME}/role-id | jq -r '.data.role_id' > ${JENKINS_SECRETS_DIR}/role-id
    vault write --format=json --force auth/approle/role/${JENKINS_APPROLE_NAME}/secret-id | jq -r '.data.secret_id' > ${JENKINS_SECRETS_DIR}/secret-id
    vault write --format=json auth/approle/login role_id="$(cat ${JENKINS_SECRETS_DIR}/role-id)" secret_id="$(cat ${JENKINS_SECRETS_DIR}/secret-id)" | jq -r '.auth.client_token' > ${JENKINS_SECRETS_DIR}/.vault-token
fi

# configure metrics approle access
METRICS_SECRETS_DIR="${METRICS_SECRETS_DIR:-/vault/secrets/metrics}"
METRICS_APPROLE_NAME="${METRICS_APPROLE_NAME:-metrics}"

if [ ! -d "${METRICS_SECRETS_DIR}" ]; then
    mkdir -p ${METRICS_SECRETS_DIR}

    vault policy write metrics-policy ${VAULT_POLICIES_DIR}/metrics-policy.hcl > /dev/null
    vault write --force auth/approle/role/${METRICS_APPROLE_NAME} token_policies="default,metrics-policy" > /dev/null
    vault read --format=json auth/approle/role/${METRICS_APPROLE_NAME}/role-id | jq -r '.data.role_id' > ${METRICS_SECRETS_DIR}/role-id
    vault write --format=json --force auth/approle/role/${METRICS_APPROLE_NAME}/secret-id | jq -r '.data.secret_id' > ${METRICS_SECRETS_DIR}/secret-id
    vault write --format=json auth/approle/login role_id="$(cat ${METRICS_SECRETS_DIR}/role-id)" secret_id="$(cat ${METRICS_SECRETS_DIR}/secret-id)" | jq -r '.auth.client_token' > ${METRICS_SECRETS_DIR}/.vault-token
fi

# configure grafana approle access
GRAFANA_SECRETS_DIR="${GRAFANA_SECRETS_DIR:-/vault/secrets/grafana}"
GRAFANA_APPROLE_NAME="${GRAFANA_APPROLE_NAME:-grafana}"

if [ ! -d "${GRAFANA_SECRETS_DIR}" ]; then
    mkdir -p ${GRAFANA_SECRETS_DIR}

    vault policy write grafana-policy ${VAULT_POLICIES_DIR}/grafana-policy.hcl > /dev/null
    vault write --force auth/approle/role/${GRAFANA_APPROLE_NAME} token_policies="default,grafana-policy" > /dev/null
    vault read --format=json auth/approle/role/${GRAFANA_APPROLE_NAME}/role-id | jq -r '.data.role_id' > ${GRAFANA_SECRETS_DIR}/role-id
    vault write --format=json --force auth/approle/role/${GRAFANA_APPROLE_NAME}/secret-id | jq -r '.data.secret_id' > ${GRAFANA_SECRETS_DIR}/secret-id
    vault write --format=json auth/approle/login role_id="$(cat ${GRAFANA_SECRETS_DIR}/role-id)" secret_id="$(cat ${GRAFANA_SECRETS_DIR}/secret-id)" | jq -r '.auth.client_token' > ${GRAFANA_SECRETS_DIR}/.vault-token
fi

# ensure all generated secrets are owned by vault
chown vault:vault -R "${VAULT_SECRETS_DIR}"

# execute the original docker-entrypoint.sh file
exec /usr/local/bin/docker-entrypoint.sh vault proxy --config=/vault/config
