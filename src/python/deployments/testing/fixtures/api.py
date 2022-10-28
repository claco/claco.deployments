import grpc._server, pytest

from deployments.api import Client, DeploymentServiceResultCode, Service, ClientServiceResponse
from deployments.grpc.deployments_pb2_grpc import DeploymentsServiceStub
from deployments.grpc.deployments_pb2 import CreateDeploymentResponse, DeploymentServiceRequestResult


@pytest.fixture
def api_service(monkeypatch) -> Service:
    def wait_for_termination(self):
        raise KeyboardInterrupt()

    monkeypatch.setattr(grpc._server._Server, "wait_for_termination", wait_for_termination)

    return Service()


@pytest.fixture
def failed_api_service(monkeypatch) -> Service:
    def wait_for_termination(self):
        raise Exception("Service failure in PyTest!")

    monkeypatch.setattr(grpc._server._Server, "wait_for_termination", wait_for_termination)

    return Service()


@pytest.fixture
def api_client(grpc_stub: DeploymentsServiceStub) -> Client:
    client = Client()
    client.service = grpc_stub

    return client


@pytest.fixture
def service_response(monkeypatch):
    response = ClientServiceResponse("Fixture Service Response", DeploymentServiceResultCode.UNSPECIFIED)

    monkeypatch.setattr(ClientServiceResponse, "from_grpc_message", lambda cls: response)

    return response


# @pytest.fixture
# def grpc_service(api_client, grpc_response, monkeypatch):
#     monkeypatch.setattr(api_client.service, "CreateDeployment", lambda self: grpc_response)

#     return api_client.service


# @pytest.fixture
# def grpc_response(grpc_result) -> CreateDeploymentResponse:
#     return CreateDeploymentResponse(result=grpc_result)


# @pytest.fixture
# def grpc_result() -> DeploymentServiceRequestResult:
#     return DeploymentServiceRequestResult()
