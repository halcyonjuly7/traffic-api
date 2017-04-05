from sanic import Sanic
import aiohttp
from .utils import DistanceCalculator, QueryHandler, CenterLocator
from sanic.response import json, raw


app = Sanic(__name__)
app.config.from_pyfile("config/dev.py")
connection = f"postgres://{app.config['DB_USERNAME']}:{app.config['DB_PASSWD']}@{app.config['DB_HOSTADDR']}/nearest"
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/nearest")
async def get_data(request):
    zip_codes = [zip_code.strip().zfill(5) for zip_code in request.args.get("zip_codes").split(",")]
    radius = request.args.get("radius", 5000)
    keyword=request.args.get("type", "restaurant")
    dist_calc = DistanceCalculator(zip_codes, connection)
    ref_points = await dist_calc.ref_points()
    center_locator = CenterLocator(ref_points)
    places = await get_places(center_locator.find_center(), keyword, radius)
    return json(places)

@app.route("/photo")
async def get_photos(request):
    place_id = request.args.get("place_id")
    logging.debug(place_id)
    max_width = request.args.get("max_width", 800)
    async with aiohttp.ClientSession() as session:
        async with session.get(app.config["PICTURES_URL"], params={"photoreference":place_id, "key":app.config["API_KEY"], "maxwidth":max_width}) as resp:
            resp_data = await resp.read()
            return raw(resp_data)
        # async with session.get(app.config["PICTURES_URL"].format(place_id, app.config["API_KEY"], max_width)) as resp:
        #     resp_data = await resp.read()
        #     return raw(resp_data)


async def get_places(coords, keyword, radius):
    data = await QueryHandler.get(app.config['PLACES_URL'],
                                  key=app.config["API_KEY"],
                                  location="{0},{1}".format(coords.lat,coords.long),
                                  radius=radius,
                                  type=keyword)
    return data






