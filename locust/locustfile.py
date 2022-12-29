import time
import datetime
import uuid
from random import randrange
from locust import FastHttpUser, task, between

class QuickstartUser(FastHttpUser):
    wait_time = between(1, 5)

    @task
    def consent(self):
        self.client.get("/consent")

    @task
    def consent_then_main(self):
        self.client.get("/consent")
        self.client.get("/main")

    @task
    def consent_then_main_then_survey(self):
        self.client.get("/consent")
        self.client.get("/main")
        self.client.get("/experiment-survey")

    @task
    def submitExperiment(self):
        self.client.get("/consent")
        self.client.get("/main")
        self.client.get("/experiment-survey")
        self.client.post("http://34.88.142.68:3000/surveys/scale", json={"userId": self.userId, "answers": [randrange(2), randrange(5), randrange(5), randrange(5)], "experimentNumber": randrange(7)})

    def on_start(self):
        self.client.get("/")
        response = self.client.post("http://34.88.142.68:3000/users/connect", json={"connectedTime": datetime.datetime.now().timestamp()})
        if response.status_code != 201:
            response.failure("User could not be created")
        try:
            self.userId = response.json()["userId"]
        except JSONDecodeError:
            response.failure("Response could not be decoded as JSON")
        except KeyError:
            response.failure("Response did not contain expected key 'userId'")