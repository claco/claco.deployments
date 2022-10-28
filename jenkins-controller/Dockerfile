FROM jenkins/jenkins

LABEL name="claco.deployments/jenkins-controller"
LABEL description="Jenkins Controller for Deployments Development"
LABEL maintainer="Chris Laco <claco@chrislaco.com>"

USER root
ADD plugins.txt ${JENKINS_HOME}/plugins.txt
RUN jenkins-plugin-cli --verbose --plugin-file ${JENKINS_HOME}/plugins.txt

USER jenkins
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV PLUGINS_FORCE_UPGRADE=true
ENV TRY_UPGRADE_IF_NO_MARKER=true
ADD jenkins.yml ${JENKINS_HOME}/jenkins.yaml

USER root
