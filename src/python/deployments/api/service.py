import logging, os, os.path, sys

from concurrent import futures
from deployments.grpc.deployments_pb2_grpc import add_DeploymentsServiceServicer_to_server, grpc as rpc
from deployments.middleware.interceptors import DeploymentEventsInterceptor, DeploymenExceptionInterceptor
from deployments.middleware.servicers import DeploymentServiceServicer
from deployments.grpc import deployments_pb2 as messages

logger = logging.getLogger(__package__)

import asyncio

# import grpc
from grpc_health.v1 import health
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server
from grpc_health.v1.health_pb2 import HealthCheckResponse
from grpc_health.v1.health import HealthServicer, OVERALL_HEALTH


class Service:
    def run(self, service_address=None) -> int:
        if not service_address:
            service_address = os.environ.get("DEPLOYMENT_SERVICE_ADDRESS", "localhost:50051")

        interceptors = []  # [DeploymentEventsInterceptor(), DeploymenExceptionInterceptor()]

        server = rpc.server(futures.ThreadPoolExecutor(max_workers=1), interceptors=interceptors)
        server.add_insecure_port(address=service_address)

        health_servicer = HealthServicer()
        deployment_servicer = DeploymentServiceServicer()

        add_DeploymentsServiceServicer_to_server(deployment_servicer, server)
        add_HealthServicer_to_server(health_servicer, server)

        health_servicer.set(OVERALL_HEALTH, HealthCheckResponse.SERVING)
        for service in messages.DESCRIPTOR.services_by_name.values():
            health_servicer.set(service.full_name, HealthCheckResponse.NOT_SERVING)

        logger.info(f"Running Deployments Server (Python): Listening on {repr(service_address)}")
        logger.info("  ↪ Press CTRL-C to stop the service")

        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.info(f"Running Remote Debugger (Python): Listening on 'localhost:5678'")

            import debugpy

            debugpy.listen(5678)
            debugpy.breakpoint()

        try:
            server.start()

            for service in messages.DESCRIPTOR.services_by_name.values():
                health_servicer.set(service.full_name, HealthCheckResponse.SERVING)

            server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Server shutdown successfully")
        except BaseException as ex:
            logger.error(f"Server shutdown unexpectedly: {repr(ex)}")

            return 1

        return 0
