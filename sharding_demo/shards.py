import hashlib
from enum import Enum
import os


class Shard(Enum):
    SHARD_1 = "shard-1"
    SHARD_2 = "shard-2"
    SHARD_3 = "shard-3"


def get_env_var(var_name: str):
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable {var_name} not set!")
    return value


DATABASE_SHARDS = {
    Shard.SHARD_1: {
        "ip": "35.193.9.250",
        "password": get_env_var("UNIVERSAL_PASSWORD"),
        "hash_match": 0,
    },
    Shard.SHARD_2: {
        "ip": "34.28.146.233",
        "password": get_env_var("UNIVERSAL_PASSWORD"),
        "hash_match": 1,
    },
    Shard.SHARD_3: {
        "ip": "35.238.33.124",
        "password": get_env_var("UNIVERSAL_PASSWORD"),
        "hash_match": 2,
    },
}
"""Database shard info, keyed by shard ID.

- ip: IP address of the database shard.
- password: Password for the database shard.
- hash_match: The hash bucket that this shard is responsible for.
"""

NUM_SHARDS = len(DATABASE_SHARDS.keys())


def get_database_shard_by_id(id: Shard):
    shard = DATABASE_SHARDS[id]
    if shard is None:
        raise ValueError(f"Shard {id} does not exist.")
    return shard


def get_shard_bucket_for_fips(fips: str):
    """Get the hash bucket for a given FIPS code."""
    fips_hex_hash = hashlib.sha1(fips.encode()).hexdigest()
    fips_hash = int(fips_hex_hash, 16)
    return fips_hash % NUM_SHARDS
