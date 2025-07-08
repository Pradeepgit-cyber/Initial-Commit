from selectors import SelectSelector

from faker import Faker
from locust import HttpUser, between, task
from socketio.async_server import task_reference_holder

from phonenumber import generate_phone_number

fake=Faker("en_IN")
class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"

    @task
    def Learning(self):
        data ={
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

        with self.client.post("api/v1/register/consumer",json=data,headers=header_auth) as response:

            if response.status_code in [200,201]:
                print("API Pass")
                res_j = response.json()           #converting response in json
                res_data = res_j['data']          #fetching data from json

                name = res_data['name']           #fetching name from data
                ph = res_data['phone_number']     #fetching phone number from data
                print(name)
                print(ph)



            else:
              print("API Fail")
              print(response.text)
              print(data['name'])
              print(data['phone_number'])

