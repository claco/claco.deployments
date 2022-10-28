FROM jenkins/ssh-agent:latest

# hadolint ignore=DL3002
USER root

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates curl git-lfs gnupg lsb-release net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -aG docker jenkins

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

HEALTHCHECK --interval=5s --timeout=1s --start-period=3s --retries=3 CMD [ "netstat", "-nlp", "|", "grep '0.0.0.0:22'" ]

ENTRYPOINT ["docker-entrypoint.sh"]
