from dataclasses import dataclass
import sqlalchemy as sql
import pandas as pd

from sharding_demo.shards import Shard, get_database_shard_by_id

# Not bothering with a full data model for responses/db contents b/c this is just a demo
@dataclass
class ShardController:
    shard: Shard
    engine: sql.engine.Engine
    connection: sql.engine.Connection
    closed = False

    @staticmethod
    def from_shard_id(shard_id: Shard):
        """Create a ShardController from a Shard enum value"""
        shard = get_database_shard_by_id(shard_id)
        conn_string = f"postgresql://sean:{shard['password']}@{shard['ip']}:5432/covid"
        engine = sql.create_engine(conn_string)
        connection = engine.connect()
        return ShardController(shard_id, engine, connection)

    def all_data_for_region(self, fips: str):
        """Get all data for a given region by fips code"""
        query = f"SELECT * FROM covid_data WHERE fips = '{fips}'"
        data = pd.read_sql_query(query, self.engine)
        return data.to_dict(orient="records")

    def close(self):
        """Close the connection to the database shard"""
        self.connection.close()
        self.engine.dispose()
        self.closed = True
