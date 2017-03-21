import sqlalchemy as sa
from aiopg.sa import create_engine

metadata = sa.MetaData()
zip_table = sa.Table("zip_codes",metadata,
                     sa.Column("id", sa.Integer, primary_key=True),
                     sa.Column("zip_code",sa.String("100")),
                     sa.Column("lat", sa.Float),
                     sa.Column("long", sa.Float))

class ModelHelper:
    def __init__(self, connection):
        self._connection = connection
        self._conn = None


    async def execute(self, command):
        async with create_engine(self._connection) as engine:
            async with engine.acquire() as conn:
                connection = await conn.execute(command)
                return list(connection)

