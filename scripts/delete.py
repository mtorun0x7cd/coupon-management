from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@<cluster-host>/")
db = client["lcss"]
collection = db["coupon_coupon"]

# Delete all documents in the collection
delete_result = collection.delete_many({})

# Print the number of deleted documents
print(f"Deleted {delete_result.deleted_count} documents.")

# Disconnect from MongoDB
client.close()
