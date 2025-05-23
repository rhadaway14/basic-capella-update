import datetime
import json
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.exceptions import DocumentNotFoundException
from couchbase.options import (
    ClusterOptions,
    UpsertOptions,
    GetOptions
)

CAPELLA_ENDPOINT = "couchbases://cb.zzi6wn-sltowod4b.cloud.couchbase.com"
USERNAME = "admin"
PASSWORD = "Password1!"
BUCKET = "test"
SCOPE = "test"
COLLECTION = "test"
# KEY = "101"
# NEW_TTL_UNIX = 1751328000

DELETED = []
UPDATED = []
NOTFOUND = []


def update_ttl(key, exp):
    global DELETED
    global UPDATED
    global NOTFOUND
    try:
        # connect
        cluster = Cluster(CAPELLA_ENDPOINT, ClusterOptions(PasswordAuthenticator(USERNAME, PASSWORD)))
        bucket = cluster.bucket(BUCKET)
        collection = bucket.scope(SCOPE).collection(COLLECTION)
        # print(collection)

        # get doc before
        before = collection.get(key, GetOptions(with_expiry=True))
        doc = before.content_as[dict]
        print(doc)
        print("ttl:", before.expiry_time)

        # edit time
        now_utc = datetime.datetime.now(datetime.UTC)
        expiration_datetime = datetime.datetime.fromtimestamp(exp, datetime.UTC)
        ttl_delta = expiration_datetime - now_utc

        # update

        if ttl_delta.total_seconds() <= 0:
            collection.remove(key)
            DELETED.append(key)

        else:
            collection.upsert(key, doc, UpsertOptions(expiry=ttl_delta))
            print(f"Updated TTL to expire in {ttl_delta.total_seconds():.0f} seconds")
            print(f"Expires at: {expiration_datetime} UTC")

            # get doc after
            after = collection.get(key, GetOptions(with_expiry=True))
            print("Updated document content:", after.content_as[dict])
            print("Updated TTL (expiration time):", after.expiry_time)
            UPDATED.append(key)
    except DocumentNotFoundException:
        print("not found")
        NOTFOUND.append(key)


with open("expiration_tsky-all.json", "r") as f:
    content = json.load(f)

for item in content["rows"]:
    print(item["key"])
    print(item["value"])
    update_ttl(item["key"], item["value"])

print("DELETED:", DELETED)
print("UPDATED:", UPDATED)
print("NOTFOUND", NOTFOUND)







