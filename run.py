import os
import aiohttp
import logging
from project.nearest import app



if __name__ == "__main__":
    app.run("0.0.0.0", port=7777)