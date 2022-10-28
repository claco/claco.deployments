## Quick Start

_**Requirements**: Docker or Podman w/ Docker Compose_

```bash
# start services defined in docker-compose.yml
make start

# open Jenkins login: username: admin
pbcopy < dist/secrets/password
make login
```

### Jenkins

The jenkins ui is at localhost:8080, and uses ./dist/secrets/{username, password]

### Prometheus

http://localhost:9090/query or http://localhost:9090/metrics with no username/password

### Grafana

http://localhost:3000/ and uses ./dist/secrets/username as the user and password
