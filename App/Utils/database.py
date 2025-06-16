import mysql.connector
from pymongo import MongoClient

# Please configure your own db
def get_sql_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = 'Project'
    )

def get_mongo_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Project']
    return db