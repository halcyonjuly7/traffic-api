import aiohttp
import logging

from sanic import Sanic
from .utils import DistanceCalculator, QueryHandler, CenterLocator
from sanic.response import json, raw
from sanic_cors import CORS, cross_origin

app = Sanic(__name__)
CORS(app)
app.config.from_pyfile("project/config/dev.py")
connection = f"postgres://{app.config['DB_USERNAME']}:{app.config['DB_PASSWD']}@{app.config['DB_HOSTADDR']}/nearest"

logger = logging.getLogger("sanic_logger")


@app.route("/nearest")
async def get_data(request):
    zip_codes = [zip_code.strip().zfill(5) for zip_code in request.args.get("zip_codes").split(",")]
    radius = request.args.get("radius", 5000)
    keyword=request.args.get("type", "restaurant")
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
    return json({"data": None})


@app.route("/photo")
async def get_photos(request):
    place_id = request.args.get("place_id")
    logging.debug(place_id)
    max_width = request.args.get("max_width", 800)
    async with aiohttp.ClientSession() as session:
        async with session.get(app.config["PICTURES_URL"], params={"photoreference":place_id, "key":app.config["API_KEY"], "maxwidth":max_width}) as resp:
            resp_data = await resp.read()
            return raw(resp_data)


async def get_places(coords, keyword, radius):
    data = await QueryHandler.get(app.config['PLACES_URL'],
                                  key=app.config["API_KEY"],
                                  location="{0},{1}".format(coords.lat,coords.long),
                                  radius=radius,
                                  type=keyword)
    return data






