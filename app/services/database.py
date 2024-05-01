from pymongo import MongoClient

client = MongoClient('mongo', 27017)  # 'mongo' is the service name defined in docker-compose.yml
db = client.db

def test_db_connection():
    return str(client.list_database_names())

def get_collection(collection_name):
    return db[collection_name]