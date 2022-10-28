import logging, typer

from deployments.api.client import Client
from deployments.api.service import Service
from deployments.cli.commands.arguments import ServiceAddressOption
from typing import Union

app = typer.Typer(no_args_is_help=True, name="service", help="Deployment Platforms Service", add_completion=False)

logger = logging.getLogger(__package__)


@app.command(help="Query the service health check status")
def check(service: Union[str, None] = None):
    result = Client().check(service).status

    logger.info(result)


@app.command(help="Run the deployment service locally")
def run(service_address: str = ServiceAddressOption()) -> int:
    return Service().run(service_address=service_address)


@app.command()
def start():
    raise NotImplementedError("service start has not been implemented!")


@app.command()
def stop():
    raise NotImplementedError("service stop has not been implemented!")
