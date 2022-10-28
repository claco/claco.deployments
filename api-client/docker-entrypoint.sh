#!/usr/bin/env bash

set -euo pipefail

if [ "$1" = "deployctl" ]; then
    exec "$@"
else
    exec deployctl "$@"
fi
