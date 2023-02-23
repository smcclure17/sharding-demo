from typing import Dict
from flask import Flask, jsonify, make_response
from markupsafe import escape
from sharding_demo.shards import Shard, get_database_shard_by_id, get_shard_bucket_for_fips
from sharding_demo.controller import ShardController
from flask import request

app = Flask(__name__)

# initialize in global scope so we don't have to reinitialize every time we make a request
# This mapping feels a little meh, but oh well.
# Mapping hash bucket --> database shard
database_shards: Dict[int, ShardController] = {
    get_database_shard_by_id(shard)["hash_match"]: ShardController.from_shard_id(shard) 
    for shard in Shard
}

@app.route("/")
def hello_from_root():
    return jsonify(message='Successfull!')

@app.route("/data/<fips>")
def test_query(fips: str):
    # TODO: Move this to middleware. Or a decorator?
    shard_bucket = get_shard_bucket_for_fips(fips)
    if shard_bucket not in database_shards.keys():
        return make_response(jsonify(error='Invalid shard found!'), 404)
    
    database_shard = database_shards[shard_bucket]
    data = database_shard.all_data_for_region(escape(fips))
    return make_response(jsonify(data), 200)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)