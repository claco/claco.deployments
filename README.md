## Quick Start

_**Requirements**: Docker or Podman w/ Docker Compose_

```bash
# start services defined in docker-compose.yml
make start

# open Jenkins login: username: admin
pbcopy < dist/secrets/password
make login
```
