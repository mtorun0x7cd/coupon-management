from pymongo import MongoClient
import random

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://<username>:<password>@<cluster-host>/"
)
db = client["lcss"]
collection = db["coupon_coupon"]
for i in range(1000):
    test = random.randint(1, 1000000)
    # Generate the document data
    document_data = {
        "_id": str(test),
        "id": test,
        "user_id": 1,
        "name": "Test" + str(test),
        "expiring_date": "2024-09-08T22:00:00.000+00:00",
        "discount_amt": 90,
        "score": 0,
        "code": "Test90",
        "comments_amt": 0,
    }

    # Insert the document into the MongoDB collection
    collection.insert_one(document_data)
    print(i)
    # Disconnect from MongoDB
client.close()
