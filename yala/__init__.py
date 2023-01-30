"""Root logger configuration."""
import logging.config
from pathlib import Path

__version__ = "3.2.0"

CONFIG_PATH = Path(__file__).parent / "logging.ini"
# The file is from this package, so we ignore the issue after checking our
# logging.ini file.
# skipcq: PY-A6006
logging.config.fileConfig(CONFIG_PATH, disable_existing_loggers=False)
