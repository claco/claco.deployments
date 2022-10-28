from deployments.api.client import DeploymentServiceResultCode, Client, ClientServiceResponse


def test_create_returns_ok(api_client: Client, service_response: ClientServiceResponse):
    service_response.code = DeploymentServiceResultCode.OK

    response = api_client.create("my-image-id")

    assert response.ok
