import hashlib
from enum import Enum

class Shard(Enum):
    SHARD_1 = "shard-1"
    SHARD_2 = "shard-2"
    SHARD_3 = "shard-3"

DATABASE_SHARDS = {
    Shard.SHARD_1: {
        "ip": "35.193.9.250",
        "password": "changeme",
        "hash_match": 0
    },
    Shard.SHARD_2: {
        "ip": "34.28.146.233",
        "password": "changeme",
        "hash_match": 1
    },
    Shard.SHARD_3: {
        "ip": "35.238.33.124",
        "password": "changeme",
        "hash_match": 2
    }
}
NUM_SHARDS = len(DATABASE_SHARDS.keys())

def get_database_shard_by_id(id: Shard):
    shard = DATABASE_SHARDS[id]
    if shard is None:
        raise ValueError(f"Shard {id} does not exist.")
    return shard

def get_shard_bucket_for_fips(fips: str):
    fips_hex_hash = hashlib.sha1(fips.encode()).hexdigest()
    fips_hash = int(fips_hex_hash, 16)
    return fips_hash % NUM_SHARDS
