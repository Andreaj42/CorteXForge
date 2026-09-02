"""Get node name identity."""

from logging import getLogger
from socket import gethostname

logger = getLogger(__name__)


def get_node_name() -> str:
    try:
        hostname = gethostname()
        return hostname
    except Exception as e:
        logger.error(f"Error getting hostname: {e}")
        return "unknown"
