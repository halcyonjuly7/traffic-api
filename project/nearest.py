import aiohttp
import logging

from sanic import Sanic
from .utils import DistanceCalculator, QueryHandler, CenterLocator
from sanic.response import json, raw
from sanic_cors import CORS, cross_origin
import os

config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "dev.py")

app = Sanic(__name__)
CORS(app)
app.config.from_pyfile(config)
connection = f"postgres://{app.config['DB_USERNAME']}:{app.config['DB_PASSWD']}@{app.config['DB_HOSTADDR']}/nearest"

logger = logging.getLogger("sanic_logger")


@app.route("/nearest")
async def get_data(request):
    zip_codes = [zip_code.strip().zfill(5) for zip_code in request.args.get("zip_codes").split(",")]
    radius = request.args.get("radius", 5000)
    keyword=request.args.get("type", "restaurant")
    logger.info(f"keyword: {keyword}")
    dist_calc = DistanceCalculator(zip_codes[:10], connection)
    zip_coords = await dist_calc.get_zip_coords()
    ref_points = await dist_calc.ref_points(zip_coords)
    center_point = CenterLocator(ref_points).find_center()
    if center_point:
        logger.info(f"Center point for {zip_codes} is {center_point}")
        places = await get_places(center_point, keyword, radius)
        return json({"data": places,
                     "zip_coords":[{"zip_code":zip_coord.zip_code,
                                    "lat": zip_coord.lat,
                                    "long": zip_coord.long} for zip_coord in zip_coords]})
    return json({"data": None,
                 "zip_coords": None})

@app.route("/nearest/next_page", methods=["GET"])
async def get_next(request):
    params = dict(key=app.config["API_KEY"],
                  page_token=request.args.get("page_token"))
    results = await QueryHandler.get(app.config['PLACES_URL'],params=params)
    return json(results)


@app.route("/photo")
async def get_photos(request):
    params = dict(photoreference=request.args.get("place_id"),
                  key=app.config["API_KEY"],
                  maxwidth=request.args.get("max_width", 1600))
    response = await QueryHandler.get(app.config["PICTURES_URL"],resp_type="read",params=params)
    return raw(response)


@app.route("/place_data")
async def place_data(request):
    params = dict(origins=f"{request.args.get('lat_1')},{request.args.get('lon_1')}",
                  destinations=f"{request.args.get('lat_2')},{request.args.get('lon_2')}")
    logger.info(params)
    response = await QueryHandler.get(app.config['PLACE_META_URL'], params=params)
    return json(response)


async def get_places(coords, keyword, radius):
    params = dict(key=app.config["API_KEY"],
                  location="{0},{1}".format(coords.lat,coords.long),
                  radius=radius,
                  type=keyword)
    data = await QueryHandler.get(app.config['PLACES_URL'],params=params)
    return data






