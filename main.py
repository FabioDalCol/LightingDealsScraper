from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def index():
    return "LightingDealsScarper!"

client = MongoClient('mongo', 27017)  
db = client.test_database  # This will create a new database if it doesn't exist

@app.route('/db_test')
def db_test():
    return str(client.list_database_names())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')