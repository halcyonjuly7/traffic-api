import collections
import itertools
import aiohttp
import asyncio
from collections import defaultdict
import logging
logging.basicConfig(level=logging.DEBUG)
from math import radians, cos, sin, asin, sqrt
from project.db.models import ModelHelper

class DistanceCalculator:
    def __init__(self, zip_codes, conn):
        self._zip_codes = zip_codes
        self._conn = conn
        self._model_helper = ModelHelper(conn)

    def _get_distances(self, coords):
        data = defaultdict(set)
        for coord in coords:
            dist_diff = coord[-1]
            for dist in coord[:2]:
                data[dist].add(dist_diff)
        return data

    async def ref_points(self):
        coordinates = collections.namedtuple("Coordinates", "zip_code lat long")
        coordinate_list = [coordinates(zip_code=data.zip_code, lat=float(data.lat), long=float(data.long)) async for
                           data in self._get_zip_coords()]
        loop = asyncio.get_event_loop()
        if len(coordinate_list) > 1:
            distance_list = await loop.run_in_executor(None,self._get_distance_list, coordinate_list)
            return self._calc_furthest_points(distance_list)
        return coordinate_list

    def _get_distance_list(self, coordinate_list):
        coords = itertools.combinations(coordinate_list, 2)
        distance_diffs = [self.calc_dist(coord[0], coord[1]) for coord in coords]
        return self._get_distances(distance_diffs)

    def _calc_furthest_points(self, distances):
        average_distance = lambda key: sum(distances[key]) / len(distances[key])
        return sorted(distances.keys(), key=average_distance, reverse=True)[:3] # top 3 furthest points


    async def _get_zip_coords(self):
        for zip_code in self._zip_codes:
            coords = await self._model_helper.execute(f"SELECT * FROM public.zip_codes WHERE zip_code =CAST({zip_code} AS VARCHAR)")
            for coord in coords:
                if coord:
                    yield coord

    def calc_dist(self, coord_1, coord_2):
        """
           Calculate the great circle distance between two points
           on the earth (specified in decimal degrees)
           """
        # convert decimal degrees to radians
        _, coord_1_lat, coord_1_long = coord_1
        _, coord_2_lat, coord_2_long = coord_2
        lon1, lat1, lon2, lat2 = map(radians, [coord_1_long, coord_1_lat, coord_2_long, coord_2_lat])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return coord_1, coord_2, c * r


class CenterLocator:
    def __init__(self, coordinate_list):
        self._coordinate_list = coordinate_list
        self._coordinates = collections.namedtuple("Coordinates", "lat long")


    def find_center(self):
        coord_length = len(self._coordinate_list)
        logging.info(f"this is the length of the coordinate list {coord_length}")
        if  coord_length == 3 or coord_length == 2:
            return self._calculate_center()
        elif coord_length == 1:
            zip_coords = self._coordinate_list[0]
            return self._coordinates(lat=zip_coords.lat, long=zip_coords.long)

    def _calculate_center(self):
        lat_average = sum(point.lat for point in self._coordinate_list) / len(self._coordinate_list)
        long_average = sum(point.long for point in self._coordinate_list) / len(self._coordinate_list)
        return self._coordinates(lat=lat_average, long=long_average)


class QueryHandler:
    @staticmethod
    async def get(url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=kwargs) as resp:
                return await resp.json()
