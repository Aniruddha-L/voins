from pymongo import MongoClient

def Delete(db):
    coll = db.list_collection_names()
    for i in coll:
        db[i].delete_many({})