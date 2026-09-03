"""Get node name identity."""

from socket import gethostname


def get_node_name() -> str:
    return gethostname()
