from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def load_tile(self):
        self.client.get("/tile/some_tile.png")
    
    @task
    def load_annotations(self):
        self.client.get("/annotations/")
