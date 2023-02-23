import pandas as pd
import sqlalchemy as sql
import logging
from sharding_demo.shards import Shard, DATABASE_SHARDS, get_shard_bucket_for_fips

logging.basicConfig(level=logging.INFO)


def shard_and_insert_covid_data():
    """Bulk insert covid data into the database shards based on the hash of the fips code.

    Data is fetched from the covidactnow.org API, and overwrites the existing data in the database.
    """
    url = "https://api.covidactnow.org/v2/counties.csv?apiKey=81d0e97ecec0406abf12c80d6cd8ec93"
    df = pd.read_csv(url, dtype={"fips": str})
    df["fips"] = df.fips.str.zfill(5)
    df["hash"] = df.fips.apply(get_shard_bucket_for_fips)
    logging.info("fetched %s rows of data...", len(df))

    for shard in Shard:
        logging.info(
            "Inserting data for shard %s", shard
        )  # f-strings threw logging error?? :(
        hash_bucket = DATABASE_SHARDS[shard]["hash_match"]
        shard_data: pd.DataFrame = df[df["hash"] == hash_bucket]
        password = DATABASE_SHARDS[shard]["password"]
        ip = DATABASE_SHARDS[shard]["ip"]

        engine = sql.create_engine(f"postgresql://sean:{password}@{ip}:5432/covid")
        shard_data.to_sql("covid_data", engine, if_exists="replace")
        engine.dispose()
