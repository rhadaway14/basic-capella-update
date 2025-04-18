import datetime
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               UpsertOptions, GetOptions)

# config
CAPELLA_ENDPOINT = "couchbases://cb.zzi6wn-sltowod4b.cloud.couchbase.com"
PASSWORD = "Password1!"
USERNAME = "admin"
BUCKET = "test"
SCOPE = "test"
COLLECTION = "test"

print(COLLECTION)

# connect
cluster = Cluster(CAPELLA_ENDPOINT, ClusterOptions(PasswordAuthenticator(USERNAME, PASSWORD)))
bucket = cluster.bucket(BUCKET)
collection = bucket.scope(SCOPE).collection(COLLECTION)
print(collection)

# get doc before
before = collection.get("101", GetOptions(with_expiry=True))
print(before.content_as[dict])
print("ttl:", before.expiry_time)

new_ttl_seconds = 600
collection.upsert("101", before.content_as[dict], UpsertOptions(expiry=datetime.timedelta(seconds=new_ttl_seconds)))
print(f"Updated TTL to {new_ttl_seconds} seconds")

# get doc after
before = collection.get("101", GetOptions(with_expiry=True))
print(before.content_as[dict])
print("ttl:", before.expiry_time)
