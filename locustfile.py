from locust import HttpUser, task, between
from uuid import uuid4
import json

class MessageUser(HttpUser):
    host = "http://localhost:5000"
    wait_time = between(1, 3)  # Random wait between 1-3 seconds between tasks
    
    def on_start(self):
        """Initialize test data"""
        self.test_message_id = None
        self.base_message = {
            "content": "Test message content",
            "sender": "test_user",
            "receiver": "test_receiver"
        }

    @task(3)  # Higher weight for GET operations
    def get_messages(self):
        """Test getting list of messages"""
        with self.client.get(
            "/api/v1/messages/",
            params={"skip": 0, "limit": 10},
            name="/messages [GET]"
        ) as response:
            if response.status_code == 200:
                messages = response.json()
                if messages and not self.test_message_id:
                    self.test_message_id = messages[0].get("id")

    @task(2)
    def create_message(self):
        """Test creating a new message"""
        with self.client.post(
            "/api/v1/messages/",
            json=self.base_message,
            name="/messages [POST]"
        ) as response:
            if response.status_code == 201:
                data = response.json()
                self.test_message_id = data.get("id")

    @task(1)
    def create_message_async(self):
        """Test creating a new message asynchronously"""
        with self.client.post(
            "/api/v1/messages/async",
            json=self.base_message,
            name="/messages/async [POST]"
        ) as response:
            if response.status_code == 201:
                data = response.json()
                self.test_message_id = data.get("id")

    @task(2)
    def get_specific_message(self):
        """Test getting a specific message"""
        if self.test_message_id:
            self.client.get(
                f"/api/v1/messages/{self.test_message_id}",
                name="/messages/{id} [GET]"
            )

    @task(1)
    def update_message(self):
        """Test updating a message"""
        if self.test_message_id:
            updated_message = self.base_message.copy()
            updated_message["content"] = f"Updated content {uuid4()}"
            self.client.put(
                f"/api/v1/messages/{self.test_message_id}",
                json=updated_message,
                name="/messages/{id} [PUT]"
            )

    @task(1)
    def delete_message(self):
        """Test deleting a message"""
        if self.test_message_id:
            self.client.delete(
                f"/api/v1/messages/{self.test_message_id}",
                name="/messages/{id} [DELETE]"
            )
            self.test_message_id = None