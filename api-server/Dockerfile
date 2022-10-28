FROM envoyproxy/envoy:v1.24-latest as envoy

FROM python:slim

LABEL name="claco.deployments/api-server"
LABEL description="Deployments API Server for Deployments Development"
LABEL maintainer="Chris Laco <claco@chrislaco.com>"

RUN apt update \
    && apt install -y build-essential supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip grpcio-tools poetry wheel

ADD dist /dist
WORKDIR /dist
RUN tar -xvzf *deployments*.tar.gz \
    && cd *deployments* \
    && pip install .

ARG DEPLOYMENT_SERVICE_HOST="[::]"
ARG DEPLOYMENT_SERVICE_PORT=50051
ARG DEPLOYMENT_SERVICE_PROXY_PORT=50052
ARG DEPLOYMENT_SERVICE_REST_PORT=50053
ARG DEPLOYMENT_SERVICE_REMOTE_DEBUGGER_PORT=5678
ARG DEPLOYMENT_SERVICE_USER=deployments
ARG DEPLOYMENT_SERVICE_GROUP=deployments
ARG DEPLOYMENT_SERVICE_DIRECTORY=/service


ENV DEPLOYMENT_SERVICE_ADDRESS=${DEPLOYMENT_SERVICE_HOST}:${DEPLOYMENT_SERVICE_PORT}

RUN useradd -ms /bin/bash ${DEPLOYMENT_SERVICE_USER}
RUN mkdir -p ${DEPLOYMENT_SERVICE_DIRECTORY}/logs \
    && chown ${DEPLOYMENT_SERVICE_USER}:${DEPLOYMENT_SERVICE_GROUP} ${DEPLOYMENT_SERVICE_DIRECTORY} \
    && touch ${DEPLOYMENT_SERVICE_DIRECTORY}/supervisor.sock

COPY --chown=${DEPLOYMENT_SERVICE_USER}:${DEPLOYMENT_SERVICE_GROUP} api-server/supervisord.conf ${DEPLOYMENT_SERVICE_DIRECTORY}/supervisord.conf
COPY --chown=${DEPLOYMENT_SERVICE_USER}:${DEPLOYMENT_SERVICE_GROUP} api-server/envoy.yaml ${DEPLOYMENT_SERVICE_DIRECTORY}/envoy.yaml
COPY --chown=${DEPLOYMENT_SERVICE_USER}:${DEPLOYMENT_SERVICE_GROUP} src/python/deployments/grpc/deployments.pb ${DEPLOYMENT_SERVICE_DIRECTORY}/deployments.pb

COPY --from=envoy /usr/local/bin/envoy* /usr/local/bin/
COPY api-server/docker-entrypoint.sh /docker-entrypoint.sh

USER ${DEPLOYMENT_SERVICE_USER}:${DEPLOYMENT_SERVICE_GROUP}

WORKDIR ${DEPLOYMENT_SERVICE_DIRECTORY}

EXPOSE ${DEPLOYMENT_SERVICE_REMOTE_DEBUGGER_PORT} ${DEPLOYMENT_SERVICE_PORT} ${DEPLOYMENT_SERVICE_PROXY_PORT} ${DEPLOYMENT_SERVICE_REST_PORT}

ENTRYPOINT [ "/docker-entrypoint.sh" ]

CMD [ "/docker-entrypoint.sh" ]
