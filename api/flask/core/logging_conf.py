import logging

logging.basicConfig(filename="access.log", 
                    level=logging.DEBUG)

logging.basicConfig(format='%(asctime)s — %(levelname)s — %(message)s', 
                    level=logging.DEBUG)
