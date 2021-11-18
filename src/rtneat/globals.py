import logging
from .tags import *

FORMAT = '%(levelname)s [%(asctime)s] %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.setLevel(INFO)
