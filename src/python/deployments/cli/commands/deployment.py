# # import deployments.api as api
import logging
import deployments.api.client as api

from deployments.cli.commands.arguments import IdArgument, ImageArgument
from typer import Typer


app = Typer(no_args_is_help=True, name="deployment", help="Deployment Platforms Deployments", add_completion=False)
client = api.Client()
logger = logging.getLogger(__package__)


@app.command(help="Create a new deployment", no_args_is_help=True)
def create(image: str = ImageArgument()):
    logger.info(f"Creating deployment {repr(image)}...")

    result = client.create(image=image)

    logger.debug(f"result={repr(result)}")

    if result.ok:
        logger.info(f"Successfully created deployment {repr(image)}")
    else:
        logger.error(f"Error creating deployment {repr(image)}")

    logger.info(result)

    result.exit()


@app.command(help="Delete an existing deployment", no_args_is_help=True)
def delete(id: str = IdArgument()):
    logger.info(f"Deleting deployment {repr(id)}...")

    result = client.delete(id=id)

    if result.ok:
        logger.info(f"Successfully deleted deployment {repr(id)}")
    else:
        logger.error(f"Error deleting deployment {repr(id)}")

    logger.info(result)

    result.exit()


@app.command(help="Queue an existing deployment", no_args_is_help=True)
def queue(id: str = IdArgument()):
    logger.info(f"Queueing deployment {repr(id)}...")

    result = client.queue(id=id)

    if result.ok:
        logger.info(f"Successfully queued deployment {repr(id)}")
    else:
        logger.error(f"Error queueing deployment {repr(id)}")

    logger.info(result)

    result.exit()
