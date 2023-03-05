import logging
import logging.config

logging.config.fileConfig(
    fname="config/log_config.conf", disable_existing_loggers=False
)
logger = logging.getLogger(__name__)
