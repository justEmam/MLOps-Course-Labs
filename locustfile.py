from locust import HttpUser, task, between

# Sample payload matching API schema
SAMPLE_PAYLOAD = {
    "CreditScore": 650,
    "Geography": "France",
    "Gender": "Male",
    "Age": 40,
    "Tenure": 3,
    "Balance": 60000.0,
    "NumOfProducts": 1,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": 50000.0,
}

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def health(self):
        self.client.get("/health")

    @task(7)
    def predict(self):
        self.client.post("/predict", json=SAMPLE_PAYLOAD)

# To run headless load test:
# locust -f locustfile.py --host http://<EC2_HOST>:8000 --headless -u 100 -r 10 --run-time 2m
# Or run the web UI:
# locust -f locustfile.py --host http://<EC2_HOST>:8000
