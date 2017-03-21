from sanic import Sanic
from .utils import DistanceCalculator, QueryHandler, CenterLocator
from sanic.response import json


app = Sanic(__name__)
app.config.from_pyfile("config/dev.py")
connection = f"postgres://{app.config['DB_USERNAME']}:{app.config['DB_PASSWD']}@{app.config['DB_HOSTADDR']}/nearest"


# @app.listener("before_server_start")
# async def prep_db(app, loop):
#     async with create_engine(connection) as engine:
#         async with engine.acquire() as conn:
#             await conn.execute("CREATE TABLE IF NOT EXISTS zip_codes ("
#                                  "id SERIAL PRIMARY KEY,"
#                                  "zip_code VARCHAR(50),"
#                                  "lat FLOAT,"
#                                  "long FLOAT);")
#             # if not zip_table.exists():
#             import csv
#             with open("gps_coordinates.csv") as coordinates:
#                 for row in csv.DictReader(coordinates):
#                     await conn.execute(zip_table.insert().values(**row))



@app.route("/nearest")
async def get_data(request):
    zip_codes = [zip_code.strip().zfill(5) for zip_code in request.args.get("zip_codes").split(",")]
    radius = request.args.get("radius", 5000)
    keyword=request.args.get("type", "restaurant")
    dist_calc = DistanceCalculator(zip_codes, connection)
    ref_points = await dist_calc.ref_points()
    center_locator = CenterLocator(ref_points)
    return json({"closest":center_locator.find_center()})


async def get_places(coords, keyword, radius):
    data = await QueryHandler.get(app.config['PLACES_URL'],
                                  key=app.config["API_KEY"],
                                  location="{0},{1}".format(coords.lat,coords.long),
                                  radius=radius,
                                  type=keyword)
    return data






