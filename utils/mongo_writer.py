from pymongo import MongoClient
import datetime
from config.settings import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def write_to_mongo(comment):
    """Write the comments to MongoDB."""
    # Establish MongoDB connection
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Insert comment into the MongoDB collection
    try:
        # Insert with unique constraint on `commentId`
        collection.update_one(
            {"commentId": comment['snippet']['topLevelComment']['id']},
            {"$set": comment['snippet']['topLevelComment']},
            upsert=True
        )
        print(f"Comment {comment['snippet']['topLevelComment']['id']} written to MongoDB")
    except Exception as e:
        print(f"An error occurred while inserting comment {comment['snippet']['topLevelComment']['id']}: {e}")

    # Close the MongoDB connection
    client.close()