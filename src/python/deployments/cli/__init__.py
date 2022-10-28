import logging, os, sys

from typing import Optional, Sequence
from deployments.cli.commands import deployment, service

deployment.app.add_typer(service.app, name="service", help="Deployment Service Commands")
logger = logging.getLogger(__package__)


def main(argv: Optional[Sequence[str]] = []) -> int:
    (log_format, log_level) = "%(message)s", logging.INFO

    exitCode = 0

    if not argv:
        argv = sys.argv[1:]

    if "--debug" in argv or os.getenv("LOG_LEVEL", "").strip().upper() == "DEBUG":
        log_format = "%(asctime)s %(name)s %(levelname)s [%(filename)s:%(lineno)s:%(funcName)s] %(message)s"
        log_level = logging.DEBUG

        if "--debug" in sys.argv:
            sys.argv.remove("--debug")

    logging.basicConfig(encoding="utf-8", datefmt="%Y-%m-%dT%H:%M:%S%z", format=log_format, level=log_level)

    try:
        exitCode = deployment.app()
    except SystemExit as ex:
        exitCode = ex.code
    except BaseException as ex:
        logger.error(ex)

        exitCode = 2

    return int(exitCode)  # type: ignore
