import logging

from deployments.api.service import Service


def test_run_returns_zero_on_success(api_service: Service, caplog):
    with caplog.at_level(logging.INFO):
        exitCode = api_service.run()

        assert exitCode == 0 and "shutdown success" in caplog.text


def test_run_returns_non_zero_on_failure(failed_api_service: Service, caplog):
    with caplog.at_level(logging.INFO):
        exitCode = failed_api_service.run()

        assert exitCode != 0 and "shutdown unexpectedly" in caplog.text


def test_run_accepts_server_address_argument(api_service: Service, caplog):
    service_address = "localhost:50000"

    with caplog.at_level(logging.INFO):
        exitCode = api_service.run(service_address=service_address)

        assert exitCode == 0 and f"Listening on {repr(service_address)}" in caplog.text
