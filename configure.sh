#!/usr/bin/env bash

set -euo pipefail

WIDTH=35

# Create local build folder
BUILD_FOLDER="${BUILD_FOLDER:-build}"
printf "%-${WIDTH}s %s\n" "Creating build folder" "[${BUILD_FOLDER}]"
mkdir -p "${BUILD_FOLDER}"

# Create local env variables folder
ENV_FILE_FOLDER="${ENV_FILE_FOLDER:-env}"
ENV_FILE_FOLDER="${BUILD_FOLDER}/${ENV_FILE_FOLDER}"
printf "%-${WIDTH}s %s\n" "Creating env files folder" "[${ENV_FILE_FOLDER}]"
mkdir -p "${ENV_FILE_FOLDER}"

# Create local logs folder
LOGS_FOLDER="${LOGS_FOLDER:-logs}"
LOGS_FOLDER="${BUILD_FOLDER}/${LOGS_FOLDER}"
printf "%-${WIDTH}s %s\n" "Creating logs folder" "[${LOGS_FOLDER}]"
mkdir -p "${LOGS_FOLDER}"

# Create local ssh folder
SSH_FOLDER="${SSH_FOLDER:-ssh}"
SSH_FOLDER="${BUILD_FOLDER}/${SSH_FOLDER}"
printf "%-${WIDTH}s %s\n" "Creating ssh folder" "[${SSH_FOLDER}]"
mkdir -p "${SSH_FOLDER}"

# Configure GitHub API Access
GITHUB_ENV_FILE="${ENV_FILE_FOLDER}/github.repository"
GITHUB_REPOSITORY_URL=`git config --get remote.origin.url`
GITHUB_REPOSITORY=`basename -s .git ${GITHUB_REPOSITORY_URL}`

if [[ ! -f "$GITHUB_ENV_FILE" ]];then
    printf "%-${WIDTH}s %s\n" "Creating GitHub repository config" "[${GITHUB_ENV_FILE}]"
    echo "GITHUB_USERNAME=${GITHUB_USERNAME:-${USER}}" > ${GITHUB_ENV_FILE}
    echo "GITHUB_REPOSITORY=${GITHUB_REPOSITORY}" >> ${GITHUB_ENV_FILE}
else
    printf "%-${WIDTH}s %s\n" "Reading GitHub repository config" "[${GITHUB_ENV_FILE}]"
    GITHUB_USERNAME=`grep GITHUB_USERNAME ${GITHUB_ENV_FILE} | cut -d '=' -f2`
    GITHUB_REPOSITORY=`grep GITHUB_REPOSITORY ${GITHUB_ENV_FILE} | cut -d '=' -f2`
fi

# Configure Vault Root Token
VAULT_ENV_FILE="${VAULT_ENV_FILE:-vault.server}"
VAULT_ENV_FILE="${ENV_FILE_FOLDER}/${VAULT_ENV_FILE}"

if [[ ! -f "$VAULT_ENV_FILE" ]];then
    printf "%-${WIDTH}s %s\n" "Creating Vault root token" "[${VAULT_ENV_FILE}: VAULT_DEV_ROOT_TOKEN_ID]"
    VAULT_DEV_ROOT_TOKEN_ID=`openssl rand -hex 16`
    echo "VAULT_DEV_ROOT_TOKEN_ID=${VAULT_DEV_ROOT_TOKEN_ID}" > ${VAULT_ENV_FILE}
else
    printf "%-${WIDTH}s %s\n" "Reading Vault root token" "[${VAULT_ENV_FILE}: VAULT_DEV_ROOT_TOKEN_ID]"
    VAULT_DEV_ROOT_TOKEN_ID=`grep VAULT_DEV_ROOT_TOKEN_ID ${VAULT_ENV_FILE} | cut -d '=' -f2`
fi

# Configure Jenkins Administrator Account
JENKINS_ADMIN_ENV_FILE="${ENV_FILE_FOLDER}/jenkins.administrator"

if [[ ! -f "$JENKINS_ADMIN_ENV_FILE" ]];then
    JENKINS_ADMIN_USERNAME="${JENKINS_ADMIN_USERNAME:-admin}"
    printf "%-${WIDTH}s %s\n" "Creating Jenkins admin password" "[${JENKINS_ADMIN_ENV_FILE}: JENKINS_ADMIN_USERNAME]"
    JENKINS_ADMIN_PASSWORD=`openssl rand -hex 16`

    echo "JENKINS_ADMIN_USERNAME=${JENKINS_ADMIN_USERNAME}" > ${JENKINS_ADMIN_ENV_FILE}
    echo "JENKINS_ADMIN_PASSWORD=${JENKINS_ADMIN_PASSWORD}" >> ${JENKINS_ADMIN_ENV_FILE}
else
    JENKINS_ADMIN_USERNAME=`grep JENKINS_ADMIN_USERNAME ${JENKINS_ADMIN_ENV_FILE} | cut -d '=' -f2`
    printf "%-${WIDTH}s %s\n" "Reading Jenkins admin password" "[${JENKINS_ADMIN_ENV_FILE}: JENKINS_ADMIN_USERNAME]"
    JENKINS_ADMIN_PASSWORD=`grep JENKINS_ADMIN_PASSWORD ${JENKINS_ADMIN_ENV_FILE} | cut -d '=' -f2`
fi

# Configure Jenkins Controller
JENKINS_CONTROLLER_ENV_FILE="${ENV_FILE_FOLDER}/jenkins.controller"

if [[ ! -f "$JENKINS_CONTROLLER_ENV_FILE" ]];then
    printf "%-${WIDTH}s %s\n" "Creating Jenkins controller config" "[${JENKINS_CONTROLLER_ENV_FILE}]"

    echo "CASC_VAULT_TOKEN=${CASC_VAULT_TOKEN:-${VAULT_DEV_ROOT_TOKEN_ID}}" > ${JENKINS_CONTROLLER_ENV_FILE}
    echo "CASC_VAULT_URL=${CASC_VAULT_URL:-http://vault-server:8200}" >> ${JENKINS_CONTROLLER_ENV_FILE}
    echo "CASC_VAULT_PATHS=${CASC_VAULT_PATHS:-cubbyhole/jenkins/administrator,cubbyhole/ssh/jenkins,cubbyhole/github}" >> ${JENKINS_CONTROLLER_ENV_FILE}
    echo "CASC_VAULT_ENGINE_VERSION=${CASC_VAULT_ENGINE_VERSION:-1}" >> ${JENKINS_CONTROLLER_ENV_FILE}
fi

# Configure Jenkins SSH Agent Keys
JENKINS_AGENT_SSH_FOLDER="${SSH_FOLDER}/jenkins"
JENKINS_AGENT_SSH_KEYPAIR_FILE="${JENKINS_AGENT_SSH_FOLDER}/id_rsa"

mkdir -p "${JENKINS_AGENT_SSH_FOLDER}"
if [[ ! -f "$JENKINS_AGENT_SSH_KEYPAIR_FILE" ]];then
    printf "%-${WIDTH}s %s\n" "Generating Jenkins SSH keys" "[${JENKINS_AGENT_SSH_KEYPAIR_FILE}]"
    ssh-keygen -t ed25519 -q -f "${JENKINS_AGENT_SSH_KEYPAIR_FILE}" -N "${VAULT_DEV_ROOT_TOKEN_ID}" -C "claco.deployments"
else
    printf "%-${WIDTH}s %s\n" "Using existing Jenkins SSH keys" "[${JENKINS_AGENT_SSH_KEYPAIR_FILE}]"
fi

# Configure Jenkins Nodes
JENKINS_NODE_ENV_FILE="${ENV_FILE_FOLDER}/jenkins.node"

if [[ ! -f "$JENKINS_NODE_ENV_FILE" ]];then
    printf "%-${WIDTH}s %s\n" "Creating Jenkins node config" "[${JENKINS_NODE_ENV_FILE}]"

    echo "JENKINS_NODE_ROOT=${JENKINS_NODE_ROOT:-/var/jenkins}" > ${JENKINS_NODE_ENV_FILE}
    echo "JENKINS_AGENT_SSH_PUBKEY=`cat ${JENKINS_AGENT_SSH_KEYPAIR_FILE}.pub`" >> ${JENKINS_NODE_ENV_FILE}
else
    printf "%-${WIDTH}s %s\n" "Reading Jenkins node config" "[${JENKINS_NODE_ENV_FILE}]"
    JENKINS_NODE_ROOT=`grep JENKINS_NODE_ROOT ${JENKINS_NODE_ENV_FILE} | cut -d '=' -f2`
fi

# Start Vault Server Container in Development Mode
export VAULT_ADDR="http://localhost:8200"
export VAULT_TOKEN="${VAULT_DEV_ROOT_TOKEN_ID}"

printf "%-${WIDTH}s %s\n" "Starting/Restarting Vault" "[vault-server: ${VAULT_ADDR}]"
docker compose up --build --detach "vault-server" &> ${LOGS_FOLDER}/docker-compose-vault-server-up.log
sleep 2 # Give old man Vault some time to stand up straight

printf "%-${WIDTH}s %s\n" "Enabling AppRole authentication"
vault auth enable approle || true

# printf "%-${WIDTH}s %s\n" "Creating Jenkins Controller AppRole"
# vault write auth/approle/role/jenkins-controller-jcasc

# Loading local secrets and settings into Vault
printf "%-${WIDTH}s %s\n" "Loading Jenkins admin credentuals" "[vault-server: cubbyhole/ssh/jenkins]"
vault kv put cubbyhole/ssh/jenkins \
    id_rsa="`cat ${JENKINS_AGENT_SSH_KEYPAIR_FILE}`" \
    id_rsa.pub="`cat ${JENKINS_AGENT_SSH_KEYPAIR_FILE}.pub`" \
        > /dev/null

printf "%-${WIDTH}s %s\n" "Loading Jenkins ssh keys" "[vault-server: cubbyhole/jenkins/administrator]"
vault kv put cubbyhole/jenkins/administrator \
    username="${JENKINS_ADMIN_USERNAME}" \
    password="${JENKINS_ADMIN_PASSWORD}" \
        > /dev/null

printf "%-${WIDTH}s %s\n" "Loading GitHub API credentials" "[vault-server: cubbyhole/github]"
vault kv put cubbyhole/github \
    username="${GITHUB_USERNAME}" \
    repository="${GITHUB_REPOSITORY}" \
    url="${GITHUB_REPOSITORY_URL}" \
    token="${GITHUB_ACCESS_TOKEN:-''}" \
        > /dev/null
