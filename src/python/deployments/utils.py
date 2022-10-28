import re


def kebab(value: str) -> str:
    """Returns a string converted to-kebab-case

    Args:
        value (str): THe string to convert to kebab case

    Returns:
        str: The value converted to kebeb case
    """
    return "-".join(
        re.sub(
            r"(\s|_|-|:|/)+",
            " ",
            re.sub(
                r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                lambda mo: " " + mo.group(0).lower(),
                value,
            ),
        ).split()
    )


class EventDecorator(object):
    """Decorator used to define how AWS EventBridge events should published"""

    def __init__(self, action: str, bus_name: str = "default"):
        """Creates a new EventDestriptor instance

        Args:
            action (str): The action that triggered the event
            bus_name (str, optional): The event bus to publish events to. Defaults to "default".
        """
        self.action = action
        self.bus_name = bus_name

    def __call__(self, function):
        event = self

        def wrapper(self, request, context):
            context.event = event

            return function(self, request, context)

        return wrapper

    def __repr__(self) -> str:
        return f"EventDecorator(action={repr(self.action)}, bus_name={repr(self.bus_name)})"
