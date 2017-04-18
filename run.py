from project.nearest import app
import logging
logger = logging.getLogger("sanic_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(app.config["STDOUT_LOG"])
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if __name__ == "__main__":
    app.run("0.0.0.0", port=7777)
