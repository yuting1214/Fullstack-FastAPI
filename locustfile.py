from locust import HttpUser, task, between
from uuid import uuid4


class MessageUser(HttpUser):
    host = "http://localhost:5000"
    wait_time = between(1, 3)

    def on_start(self):
        self.test_message_id = None
        self.base_message = {"content": "Test message content"}

    @task(3)
    def get_messages(self):
        with self.client.get(
            "/api/v1/messages/",
            params={"skip": 0, "limit": 10},
            name="/messages [GET]",
        ) as response:
            if response.status_code == 200:
                messages = response.json()
                if messages and not self.test_message_id:
                    self.test_message_id = messages[0].get("id")

    @task(2)
    def create_message(self):
        with self.client.post(
            "/api/v1/messages/",
            json=self.base_message,
            name="/messages [POST]",
        ) as response:
            if response.status_code == 201:
                self.test_message_id = response.json().get("id")

    @task(2)
    def get_specific_message(self):
        if self.test_message_id:
            self.client.get(
                f"/api/v1/messages/{self.test_message_id}",
                name="/messages/{id} [GET]",
            )

    @task(1)
    def update_message(self):
        if self.test_message_id:
            updated = {"content": f"Updated content {uuid4()}"}
            self.client.put(
                f"/api/v1/messages/{self.test_message_id}",
                json=updated,
                name="/messages/{id} [PUT]",
            )

    @task(1)
    def delete_message(self):
        if self.test_message_id:
            self.client.delete(
                f"/api/v1/messages/{self.test_message_id}",
                name="/messages/{id} [DELETE]",
            )
            self.test_message_id = None
