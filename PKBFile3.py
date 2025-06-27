from locust import HttpUser, between, task
from socketio.async_server import task_reference_holder


class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"

    @task
    def Newlearning(self):
        data = {
            "name": "Pradeep",
            "phone_number": "8765432100",
            "sms_channel": "1",
            "receive_updates": "1"
        }
        Header_auth = {
            "Api-Secret": "hudle-api1798@prod",
            "x-app-id": "TP1A.220905.001",
            "Content-Type": "application/json"
        }

        with self.client.post("api/v1/register/consumer",json=data,headers=Header_auth) as response:
          if response.status_code in (200,201):
              print("API Pass")
          else:
              print("API Fail")
              print(response.text)