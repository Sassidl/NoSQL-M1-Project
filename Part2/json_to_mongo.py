import json
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "project")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "companies")


def insert_documents(json_file: str) -> None:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    with open(json_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
                collection.insert_one(doc)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_mongo.py <cleaned_json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    insert_documents(json_file)
    print("✅ Data inserted into MongoDB successfully")
