import logging, os
import deployments.grpc.deployments_pb2 as messages
import deployments.grpc.deployments_pb2_grpc as service

from deployments.utils import kebab, EventDecorator as event

from jenkins import Jenkins
from jinja2 import Template

logger = logging.getLogger(__package__)


class DeploymentServiceServicer(service.DeploymentsServiceServicer):
    @event("create")
    def CreateDeployment(self, request, context):
        deployments_folder: str = "deployments"
        image = request.image

        logger.debug(f"image={repr(image)}")

        result = messages.DeploymentServiceRequestResult()

        deployment = messages.Deployment(id=f"{deployments_folder}/{kebab(image)}", image=image)

        templates_directory = os.path.abspath(os.path.join(__file__, "../templates"))
        template_file = os.path.join(templates_directory, "jenkins.xml.j2")

        logger.debug(f"templates_directory={repr(templates_directory)}, template_file={repr(template_file)}")

        with open(template_file) as file:
            template = Template(source=file.read())
            job = template.render(image=image)

            logger.debug(f"Creating pipeline {repr(deployment.id)} in Jenkins")
            logger.debug(f"job={repr(job)}")

            try:
                jenkins_server = self.__jenkins()
                jenkins_server.create_folder(folder_name=deployments_folder, ignore_failures=True)
                jenkins_server.create_job(name=deployment.id, config_xml=job)

                result.code = messages.DSRC_OK
                deployment.status = messages.DS_CREATED
            except Exception as ex:
                logger.debug(str(ex))

        return messages.CreateDeploymentResponse(result=result, deployment=deployment)

    @event("delete")
    def DeleteDeployment(self, request, context):
        id = request.id

        logger.debug(f"id={repr(id)}")

        result = messages.DeploymentServiceRequestResult()

        deployment = messages.Deployment(id=id)

        context.send_initial_metadata(
            (
                ("checksum", "foop"),
                ("retry", "true"),
            )
        )

        try:
            jenkins_server = self.__jenkins()
            jenkins_server.delete_job(name=id)

            result.code = messages.DSRC_OK
            deployment.status = messages.DS_DELETED
        except Exception as ex:
            logger.debug(str(ex))

        return messages.DeleteDeploymentResponse(result=result, deployment=deployment)

    @event("queue")
    def QueueDeployment(self, request, context):
        id = request.id

        logger.debug(f"id={repr(id)}")

        result = messages.DeploymentServiceRequestResult()

        deployment = messages.Deployment(id=id)

        try:
            jenkins_server = self.__jenkins()

            queue_item_number = jenkins_server.build_job(name=id, parameters={"image": None})
            queue_item = jenkins_server.get_queue_item(number=queue_item_number)

            result.code = messages.DSRC_OK
            deployment.status = messages.DS_QUEUED
        except Exception as ex:
            logger.debug(str(ex))

        return messages.QueueDeploymentResponse(result=result, deployment=deployment)

    def __jenkins(self) -> Jenkins:
        url = os.environ.get("JENKINS_URL", "http://jenkins-controller:8080")
        username = os.environ.get("JENKINS_ADMIN_USERNAME", None)
        password = os.environ.get("JENKINS_ADMIN_PASSWORD", None)

        return Jenkins(url=url, username=username, password=password)
