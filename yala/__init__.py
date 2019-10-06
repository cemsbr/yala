"""Root logger configuration."""
import logging.config
from pathlib import Path

__version__ = '1.8.0'

CONFIG_PATH = Path(__file__).parent / 'logging.ini'
logging.config.fileConfig(str(CONFIG_PATH), disable_existing_loggers=False)
