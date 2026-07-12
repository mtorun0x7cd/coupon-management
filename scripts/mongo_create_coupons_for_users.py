from pymongo import MongoClient
import random
import string
from datetime import datetime
import uuid

# Connect to MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@<cluster-host>/")
db = client["lcss"]
user_collection = db["auth_user"]
coupon_collection = db["coupon_coupon"]

# Fetch existing users
existing_users = list(user_collection.find())

# Generate and insert coupons for each user
for user in existing_users:
    user_id = user["id"]
    name = user["username"]

    # Create and assign 10 unique coupons per user
    for i in range(5):
        test = random.randint(1, 1000000)
        expiring_date = datetime(2020, 9, 8, 22, 0, 0)
        discount_amt = 20
        score = 0
        code = f"{name}{discount_amt}"
        comments_amt = 0

        document_data = {
            "_id": str(uuid.uuid4()),  # Generate unique UUID as _id
            "id": user_id + test,
            "user_id": user_id,
            "name": name,
            "expiring_date": expiring_date,
            "discount_amt": discount_amt,
            "score": score,
            "code": code,
            "comments_amt": comments_amt,
        }

        # Insert the coupon document
        coupon_collection.insert_one(document_data)

# Disconnect from MongoDB
client.close()
