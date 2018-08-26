"""Root logger configuration."""
from pathlib import Path
import logging.config

__version__ = '1.7.0'

CONFIG_PATH = Path(__file__).parent / 'logging.ini'
logging.config.fileConfig(str(CONFIG_PATH), disable_existing_loggers=False)
