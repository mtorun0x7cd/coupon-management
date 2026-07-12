import psycopg2
from psycopg2 import Error
import random
import string
import datetime

# PostgreSQL connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "coupon"
DB_USER = "mtorun0x7cd"
DB_PASSWORD = "<db-password>"

# Number of coupons to create
num_coupons = 1000

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Get the existing user IDs from the auth_user table
    cursor.execute("SELECT id FROM auth_user")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Generate and insert coupon records
    for i in range(1, num_coupons + 1):
        user_id = random.choice(user_ids)
        name = "Coupon " + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        expiring_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))
        discount_amt = random.randint(1, 100)
        score = 0
        code = f"{name}{discount_amt}"
        comments_amt = 0

        query = """
        INSERT INTO coupon_coupon (user_id, name, expiring_date, discount_amt, score, code, comments_amt)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            name,
            expiring_date,
            discount_amt,
            score,
            code,
            comments_amt
        )
        cursor.execute(query, values)

        print(f"Coupon {i} created for User {user_id}.")

    # Commit the changes to the database
    connection.commit()

    print(f"{num_coupons} coupon records created successfully.")

except (Exception, Error) as error:
    print(f"Error while connecting to PostgreSQL: {error}")

finally:
    # Close the database connection and cursor
    if connection:
        cursor.close()
        connection.close()
