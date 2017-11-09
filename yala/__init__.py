"""Root logger configuration."""
from pathlib import Path
import logging.config

logging.config.fileConfig(Path(__file__).parent / 'logging.ini',
                          disable_existing_loggers=False)
