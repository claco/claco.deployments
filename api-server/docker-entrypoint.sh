#!/usr/bin/env bash

set -eom pipefail

trap HUP INT QUIT TERM

if [ "$1" = "deployctl" ]; then
    exec "$@"
else
    exec /usr/bin/supervisord &
    sleep 1

    supervisorctl start service
    supervisorctl start proxy

    fg %1
fi
