# https://www.mongodb.com/docs/drivers/pymongo/?_ga=2.110152259.730470487.1718575439-130080192.1716311007&_gac=1.124346872.1718575439.CjwKCAjwmrqzBhAoEiwAXVpgovPwix2BZKpR39yNj-KbftTkqdyl5MM_ZI4SDgf_FBIWce_FyRLteRoCx1MQAvD_BwE%252525252525252525253Futm_source%252525252525252525253Dgoogle

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder with your Atlas connection string
uri = "mongodb://localhost:27017/"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)