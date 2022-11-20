from pymongo import MongoClient
import json


def init_db():
    # Creating a pymongo client
    client = MongoClient('localhost', 27017)

    # Getting the database instance
    db = client['afd_tweet_analyzer']
    print("Database created........")

    # Verification
    print("List of databases after creating new one")
    print(client.list_database_names())

    return db

def init_collection(db):
    # Creating a collection
    collection = db['tweets']
    print("Collection created........")
    return collection



if __name__ == '__main__':
    db = init_db()

    collection = init_collection(db)

    file = open(
        '../data-warehouse/old_cps_for_testing/json_files/part-00000-551aaf99-258a-4867-a489-2dd8c706fc9f-c000.json', encoding='utf-8')
    data = json.load(file)

    result = collection.insert_many(data)

    # Iterating through the json
    # list
    for i in data:
        print(i)

    # Closing file
    file.close()




