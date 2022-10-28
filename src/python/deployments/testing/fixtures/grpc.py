import pytest


@pytest.fixture(scope="module")
def grpc_add_to_server():
    import deployments.grpc.deployments_pb2_grpc as service

    return service.add_DeploymentsServiceServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    import deployments.grpc.deployments_pb2 as messages
    import deployments.grpc.deployments_pb2_grpc as service

    class MockServicer(service.DeploymentsServiceServicer):
        def CreateDeployment(self, request, context) -> messages.CreateDeploymentResponse:
            return messages.CreateDeploymentResponse()

    return MockServicer()


@pytest.fixture(scope="module")
def grpc_stub_cls(grpc_channel):
    import deployments.grpc.deployments_pb2_grpc as service

    return service.DeploymentsServiceStub
