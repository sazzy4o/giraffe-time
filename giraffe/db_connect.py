import os

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

dirname = os.path.dirname(__file__)

cloud_config= {
        'secure_connect_bundle': os.path.join(dirname, '../secure-connect-giraffe-time.zip')
}
auth_provider = PlainTextAuthProvider(os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'))
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
    print(row[0])
else:
    print("An error occurred.")