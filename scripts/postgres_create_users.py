import psycopg2
from psycopg2 import Error
import uuid
import datetime

# PostgreSQL connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "coupon"
DB_USER = "mtorun0x7cd"
DB_PASSWORD = "<db-password>"
# Number of user records to create
num_users = 100

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Generate and insert user records
    for i in range(1, num_users + 1):
        password = (
            "pbkdf2_sha256$390000$5Vy02HKoDvq2PBu1sVXpOM$+lTXr+A6wnQsTNMYX4eRM7TkBs"
        )
        last_login = datetime.datetime.now()
        is_superuser = False
        username = f"user{i}"
        first_name = f"First{i}"
        last_name = f"Last{i}"
        email = f"user{i}@example.com"
        is_staff = False
        is_active = True
        date_joined = datetime.datetime.now()

        query = """
        INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email,
        is_staff, is_active, date_joined)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        values = (
            password,
            last_login,
            is_superuser,
            username,
            first_name,
            last_name,
            email,
            is_staff,
            is_active,
            date_joined,
        )
        cursor.execute(query, values)
        user_id = cursor.fetchone()[0]

        print(f"User {user_id} created.")

    # Commit the changes to the database
    connection.commit()

    print(f"{num_users} user records created successfully.")

except (Exception, Error) as error:
    print(f"Error while connecting to PostgreSQL: {error}")

finally:
    # Close the database connection and cursor
    if connection:
        cursor.close()
        connection.close()
