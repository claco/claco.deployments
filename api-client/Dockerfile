FROM python:slim

LABEL name="claco.deployments/api-client"
LABEL description="Deployments API Client for Deployments Development"
LABEL maintainer="Chris Laco <claco@chrislaco.com>"

RUN apt update \
    && apt install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip grpcio-tools poetry wheel

ADD dist /dist

WORKDIR /dist

RUN tar -xvzf *deployments*.tar.gz \
    && cd *deployments* \
    && pip install .

ARG DEPLOYMENT_SERVICE_HOST=localhost
ARG DEPLOYMENT_SERVICE_PORT=50051
ARG DEPLOYMENT_CLIENT_USER=deployments
ARG DEPLOYMENT_CLIENT_GROUP=deployments
ARG DEPLOYMENT_CLIENT_DIRECTORY=/client

ENV DEPLOYMENT_SERVICE_ADDRESS=${DEPLOYMENT_SERVICE_HOST}:${DEPLOYMENT_SERVICE_PORT}

RUN useradd -ms /bin/bash ${DEPLOYMENT_CLIENT_USER}

RUN mkdir -p ${DEPLOYMENT_CLIENT_DIRECTORY} \
    && chown ${DEPLOYMENT_CLIENT_USER}:${DEPLOYMENT_CLIENT_GROUP} ${DEPLOYMENT_CLIENT_DIRECTORY}

COPY api-client/docker-entrypoint.sh /docker-entrypoint.sh

USER ${DEPLOYMENT_CLIENT_USER}:${DEPLOYMENT_CLIENT_GROUP}

WORKDIR ${DEPLOYMENT_CLIENT_DIRECTORY}

ENTRYPOINT [ "/docker-entrypoint.sh" ]

CMD [ "/docker-entrypoint.sh" ]
