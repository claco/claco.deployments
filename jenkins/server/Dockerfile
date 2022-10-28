FROM jenkins/jenkins:latest

USER root

COPY plugins.txt ${JENKINS_HOME}/plugins.txt
RUN jenkins-plugin-cli --verbose --plugin-file "${JENKINS_HOME}/plugins.txt"

USER jenkins

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true
ENV PLUGINS_FORCE_UPGRADE=true
ENV TRY_UPGRADE_IF_NO_MARKER=true COLLECT_DISK_USAGE=true COLLECTING_METRICS_PERIOD_IN_SECONDS=300
COPY jenkins.yml ${JENKINS_HOME}/jenkins.yaml
COPY seed.groovy ${JENKINS_HOME}/seed.groovy

HEALTHCHECK --interval=5s --timeout=1s --start-period=3s --retries=3 CMD [ "curl", "http://localhost:8080" ]
