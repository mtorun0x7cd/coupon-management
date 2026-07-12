from locust import HttpUser, task, between
import psycopg2
from psycopg2 import Error


class PostgresUser(HttpUser):
    wait_time = between(1, 2)  # Time between consecutive tasks

    @task
    def perform_query(self):
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="coupon",
            user="mtorun0x7cd",
            password="<db-password>",
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Perform a sample database query
        try:
            cursor.execute("SELECT * FROM coupon_coupon")
            result = cursor.fetchall()
        except (Exception, Error) as error:
            print(f"Error while performing query: {error}")

        # Close the database connection and cursor
        cursor.close()
        connection.close()
