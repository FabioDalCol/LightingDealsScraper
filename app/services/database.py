from pymongo import MongoClient

client = MongoClient('mongo', 27017)  # 'mongo' is the service name defined in docker-compose.yml
db = client.test_database  # This will create a new database if it doesn't exist

def test_db_connection():
    return str(client.list_database_names())