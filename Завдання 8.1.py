import logging

logging.basicConfig(level=logging.INFO, filename="logfile.log", filemode="a", format="%(name)s - %(levelname)s - %(message)s - %(asctime)s",   datefmt="%Y-%m-%d")

logging.info("info message")