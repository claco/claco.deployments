import grpc, logging, os, sys
import deployments.grpc.deployments_pb2 as messages
import deployments.grpc.deployments_pb2_grpc as service

from enum import auto, Flag
from google.protobuf import json_format
from grpc_health.v1.health import OVERALL_HEALTH
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_health.v1.health_pb2 import HealthCheckResponse

logger = logging.getLogger(__package__)


class DeploymentServiceResultCode(Flag):
    UNSPECIFIED = auto()
    OK = auto()
    ERROR = auto()

    def __repr__(self) -> str:
        return repr(self.name)


class DeploymentResult(Flag):
    UNSPECIFIED = auto()
    OK = auto()
    ERROR = auto()

    def __repr__(self) -> str:
        return repr(self.name)


class DeploymentStatus(Flag):
    UNSPECIFIED = auto()
    CREATED = auto()
    QUEUED = auto()
    STARTED = auto()
    COMPLETED = auto()
    DELETED = auto()

    def __repr__(self) -> str:
        return repr(self.name)


class ClientServiceResponse:
    @classmethod
    def from_grpc_message(cls, message):
        code = DeploymentServiceResultCode.UNSPECIFIED
        message_result_code = 0
        message_result_message = None
        deployment = None

        if message:
            message_result_code = message.result.code
            message_result_message = message.result.message
            deployment = json_format.MessageToDict(message.deployment)

        enum_name, enum_descriptor = messages.DESCRIPTOR.enum_types_by_name.items()[0]

        for k, v in enum_descriptor.values_by_name.items():
            enum_value = str(k).split("_", maxsplit=1)[1]

            if int(v.number) == int(message_result_code):
                code = DeploymentServiceResultCode[enum_value]

        return cls(code=code, deployment=deployment, message=str(message_result_message))

    @classmethod
    def from_grpc_error(cls, error):
        if error.args:
            response = error.args[0].response
        else:
            response = None

        result = cls.from_grpc_message(message=response)
        result.code = DeploymentServiceResultCode.ERROR
        result.message = error.details()

        return result

    def __init__(self, code: DeploymentServiceResultCode, deployment=None, message: str | None = None) -> None:
        self.code = code
        self.message = message
        self.deployment = deployment

    def __repr__(self) -> str:
        return f"<{__class__.__name__} code={repr(self.code)}, deployment={repr(self.deployment)}, message={repr(self.message)}>"

    @property
    def ok(self) -> bool:
        if self.code == DeploymentServiceResultCode.OK:
            return True
        else:
            return False

    @property
    def exit_code(self) -> int:
        if not self.ok:
            return 2

        return 0

    def exit(self):
        sys.exit(self.exit_code)


class Client:
    def __init__(self, service_address: str | None = None) -> None:
        if not service_address:
            service_address = os.environ.get("DEPLOYMENT_SERVICE_ADDRESS", "localhost:50051")

        self.channel = grpc.insecure_channel(target=service_address)
        self.service = service.DeploymentsServiceStub(channel=self.channel)

    def check(self, service: str | None = OVERALL_HEALTH) -> HealthCheckResponse:
        health_service = health_pb2_grpc.HealthStub(grpc.insecure_channel("localhost:50051"))

        request = health_pb2.HealthCheckRequest(service=service)
        logger.debug(repr(request))

        try:
            response = health_service.Check(request)
            logger.debug(f"response={repr(response).strip()}")

            return response
        except grpc.RpcError as ex:
            logger.debug(str(ex))

        return HealthCheckResponse(status=HealthCheckResponse.UNKNOWN)

    def create(self, image: str | None = None) -> ClientServiceResponse:
        logger.debug(f"image={repr(image)}")

        request = messages.CreateDeploymentRequest(image=image)
        logger.debug(f"request={repr(request).strip()}")

        try:
            response = self.service.CreateDeployment(request)

            return ClientServiceResponse.from_grpc_message(response)
        except grpc.RpcError as ex:
            return ClientServiceResponse.from_grpc_error(ex)

    def delete(self, id: str) -> ClientServiceResponse:
        logger.debug(f"id={repr(id)}")

        request = messages.DeleteDeploymentRequest(id=id)
        logger.debug(f"request={repr(request).strip()}")

        try:
            # response = self.service.DeleteDeployment(request)
            response, call = self.service.DeleteDeployment.with_call(request)
            logger.info(call.initial_metadata())

            return ClientServiceResponse.from_grpc_message(response)
        except grpc.RpcError as ex:
            return ClientServiceResponse.from_grpc_error(ex)

    def queue(self, id: str) -> ClientServiceResponse:
        logger.debug(f"id={repr(id)}")

        request = messages.QueueDeploymentRequest(id=id)
        logger.debug(f"request={repr(request).strip()}")

        try:
            response = self.service.QueueDeployment(request)

            return ClientServiceResponse.from_grpc_message(response)
        except grpc.RpcError as ex:
            return ClientServiceResponse.from_grpc_error(ex)
