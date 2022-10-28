import boto3, logging, os
import deployments.grpc.deployments_pb2 as messages

from deployments.grpc.deployments_pb2 import DeploymentServiceRequestResult
from deployments.utils import EventDecorator
from grpc import ServicerContext, StatusCode
from grpc_interceptor import ServerInterceptor
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Struct
from typing import Callable, Any

logger = logging.getLogger(__package__)

if logger.getEffectiveLevel() == logging.DEBUG:
    # Quit please we're logging over here
    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("botocore").setLevel(logging.INFO)


class DeploymentEventsInterceptor(ServerInterceptor):
    def intercept(self, method: Callable, request: Any, context: ServicerContext, method_name: str) -> Any:
        logger.info(f"Executing {__class__.__name__}")
        logger.debug(f"method_name={repr(method_name)}, request={repr(request)}")

        response = super().intercept(method, request, context, method_name)
        logger.debug(f"response={repr(response)}")

        event: EventDecorator = context.event  # type: ignore
        logger.debug(f"event={repr(event)}")

        detail = Struct()
        detail.update({"action": event.action})
        result: DeploymentServiceRequestResult = response.result

        if response.deployment:
            detail.update({"deployment": json_format.MessageToDict(response.deployment)})
            logger.debug(f"deployment={response.deployment}")

        try:
            enum_value = messages.DeploymentServiceResultCode.DESCRIPTOR.values_by_number.get(result.code).name
            detail.update({"result": "".join(enum_value.split("_", 1)[1:]).replace("_", "-").lower()})
        except Exception as ex:
            logger.debug(f"Enum name not found for value {repr(response.result.code)}")
            logger.error(str(ex))

        service_event = messages.DeploymentServiceEvent(event=method_name.lstrip("/").replace("/", "."), detail=detail)
        logger.debug(f"event={repr(service_event)}")

        result.events.extend([service_event])

        try:
            aws_endpoint_url = os.getenv("AWS_ENDPOINT_URL", None)
            aws_region_name = os.getenv("AWS_REGION", "us-east-1")

            aws_client = boto3.client("events", endpoint_url=aws_endpoint_url, region_name=aws_region_name)
            aws_response = aws_client.put_events(
                Entries=[
                    {
                        "Source": f"deployments.{event.action}",
                        "DetailType": "Deployments Service Response",
                        "Detail": json_format.MessageToJson(service_event),
                        "EventBusName": event.bus_name,
                    }
                ]
            )

            logger.debug(f"aws.event={repr(aws_response)}")
        except BaseException as ex:
            logger.error(f"Error publishing event: {ex}")

        return response


class DeploymenExceptionInterceptor(ServerInterceptor):
    def intercept(self, method: Callable, request: Any, context: ServicerContext, method_name: str) -> Any:
        logger.info(f"Executing {__class__.__name__}")
        logger.debug(f"method_name={repr(method_name)}, request={str(request)}")

        response = super().intercept(method, request, context, method_name)
        logger.debug(f"response={repr(response)}")

        event: EventDecorator = context.event  # type: ignore
        logger.debug(f"event={repr(event)}")

        if not context.code():
            context.set_code(StatusCode.INTERNAL)
            context.set_details("An unhandled exception has occurred")

            result = response.result
            result.code = messages.DSRC_ERROR
            result.message = context.details()

        return response
