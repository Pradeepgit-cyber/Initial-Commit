from locust import HttpUser, between, task
from socketio.async_server import task_reference_holder

from Regd import fake
from phonenumber import generate_phone_number


class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"


    @task
    def learning(self):
        data = {
            "name": fake.name(),
            "phone_number": generate_phone_number(),
            "sms_channel": "1",
            "receive_updates": "1"
        }

        header_auth = {
            "Api-Secret": "hudle-api1798@prod",
            "x-app-id": "TP1A.220905.001",
            "Content-Type": "application/json"
        }

        with self.client.post("api/v1/register/consumer",json = data,headers = header_auth) as response:
            if response.status_code in [200,201]:
                print("API PASS")
                print("data:"  f"{data['phone_number']}")
                print(response.json())


            else:
                print("API FAIL")

                print(response.text)



