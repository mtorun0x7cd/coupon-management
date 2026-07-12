from pymongo import MongoClient
import random
import string
from datetime import datetime

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://<username>:<password>@<cluster-host>/"
)
db = client["lcss"]
collection = db["auth_user"]

# Generate and insert user documents
for i in range(2, 101):
    user_id = i
    password = "".join(random.choices(string.ascii_letters + string.digits, k=64))
    last_login = datetime.utcnow()
    is_superuser = False
    username = "".join(random.choices(string.ascii_letters, k=8))
    first_name = "".join(random.choices(string.ascii_letters, k=5))
    last_name = "".join(random.choices(string.ascii_letters, k=6))
    email = f"{username}@example.com"
    is_staff = False
    is_active = True
    date_joined = datetime.utcnow()

    document_data = {
        "_id": f"{user_id:0>24x}",
        "id": user_id,
        "password": password,
        "last_login": last_login,
        "is_superuser": is_superuser,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "is_staff": is_staff,
        "is_active": is_active,
        "date_joined": date_joined,
    }

    collection.insert_one(document_data)
    print(i)
# Disconnect from MongoDB
client.close()
