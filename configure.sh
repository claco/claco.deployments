#!/usr/bin/env bash

set -euo pipefail

SECRETSDIR="${SECRETSDIR:-./dist/secrets}"

mkdir -p ${SECRETSDIR}

echo "Generating username in '${SECRETSDIR}/username'"
rm -rf ${SECRETSDIR}/username
echo "admin" > ${SECRETSDIR}/username

echo "Generating password secret in '${SECRETSDIR}/password'"
rm -rf ${SECRETSDIR}/password
openssl rand -hex 16 > ${SECRETSDIR}/password

echo "Generating ssh secret in '${SECRETSDIR}/id_rsa'"
rm -rf ${SECRETSDIR}/id_rsa*
ssh-keygen -t ed25519 -q -f ${SECRETSDIR}/id_rsa -N "$(cat ${SECRETSDIR}/password)" -C "claco.deployments"
