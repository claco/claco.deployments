from typer import Argument, Option


def IdArgument(default=..., **kwargs):
    return Argument(default, help="Deployment id returned by create", **kwargs)


def ImageArgument(default=..., **kwargs):
    return Argument(default, help="Docker image to deploy")


def ServiceAddressOption(default=None, **kwargs):
    return Option(default, help="Deployment service address", metavar="host:port")
