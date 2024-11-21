import logging
import os

from dotenv import load_dotenv

log = logging.getLogger(__name__)

load_dotenv()

KRONOTERM_CLOUD_USER = os.getenv("KRONOTERM_CLOUD_USER")
KRONOTERM_CLOUD_PASSWORD = os.getenv("KRONOTERM_CLOUD_PASSWORD")
