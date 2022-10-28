import deployments.grpc.deployments_pb2 as messages
from deployments.grpc.deployments_pb2_grpc import DeploymentsServiceStub


def test_ehlo(grpc_stub: DeploymentsServiceStub):
    request = messages.CreateDeploymentRequest(image="my-image")

    response = grpc_stub.CreateDeployment(request=request)

    assert response
