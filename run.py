from project.nearest import app
import logging
import sys
logger = logging.getLogger("sanic_logger")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(app.config["STDOUT_LOG"])
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == "__main__":
    app.run("0.0.0.0", port=7777, debug=True)
