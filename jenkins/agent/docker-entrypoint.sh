#!/usr/bin/env bash
# shellcheck shell=bash

set -eau pipefail

JENKINS_AGENT_SSH_PUBKEY="$(cat /run/secrets/id_rsa.pub)"

export JENKINS_AGENT_SSH_PUBKEY

exec setup-sshd
