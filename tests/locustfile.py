from locust import HttpUser, task, between


# Locust User class
class CouponUser(HttpUser):
    wait_time = between(1, 3)  # Time between consecutive tasks

    @task
    def view_coupon(self):
        # Simulate users accessing the coupon endpoint
        self.client.get(
            "/search_coupons/?csrfmiddlewaretoken=<csrf-token>&search_query=test"
        )
