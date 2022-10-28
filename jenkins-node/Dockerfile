FROM jenkins/ssh-agent

LABEL name="claco.deployments/jenkins-node"
LABEL description="Jenkins SSH Agent Node for Deployments Development"
LABEL maintainer="Chris Laco <claco@chrislaco.com>"

USER root

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates curl git-lfs gnupg lsb-release \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -aG docker jenkins

ENV JENKINS_NODE_ROOT=/var/jenkins

RUN mkdir -p ${JENKINS_NODE_ROOT}  && chown jenkins:jenkins ${JENKINS_NODE_ROOT}
