A simple example of database sharding using PostgreSQL and a simple hashing function. API built in Flask and exposed using AWS Lambdas deployed through Serverless.


# Setup 
To run locally:

## Run terraform to setup GCP infrastructure:
Set up the scaffolding using terraform:

```IPV4_ADRESS=foo UNIVERSAL_PASSWORD=bar terraform apply```

where "foo" is your local ip address and "bar" is the password to use for all instances.
Your local IP address is required to authorize a connection to the PostgreSQL instances. 

This password is also used elsewhere in the code, so run:

`export UNIVERSAL_PASSWORD=bar`

to set the variable. TODO: this needs to be added to Serverless/AWS secret manager for official deploys.

## Add databases to SQL servers manually (TODO: add this to terraform):
For each shard instance, go to:

- databases --> create database --> set name to "covid" --> create


## Populate the database shards:
run `pip install -r requirements.txt`

run `pip install -r requirements-dev.txt`

In an interactive Python (ipython) session run:

```python
from sharding_demo.utils.fetching import shard_and_insert_covid_data
shard_and_insert_covid_data()
```

This will fetch data from the https://www.covidactnow.org/data-api API and insert it into the correct database shards.

## Run serverless locally:
run `serverless wsgi serve`

Get data for a county, e.g. Middlesex, MA, via: `http://localhost:5000/data/25017`


--------------

## TODOS:
- Add a data model for requests/responses then create OpenAPI documentation.
- Add Environment variables to Serverless/AWS to complete deploy steps.
