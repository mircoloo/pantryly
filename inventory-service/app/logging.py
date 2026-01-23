import logging

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
# we need addHandler to combine handler with logger
logger.addHandler(console_handler)

#### formatter ####
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
 )
# we need setFormatter to combine handler with handler
console_handler.setFormatter(formatter)

