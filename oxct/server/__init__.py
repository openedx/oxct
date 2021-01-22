import logging
import os

logging.basicConfig(level=os.environ.get("OXCT_LOG_LEVEL", logging.WARNING))
