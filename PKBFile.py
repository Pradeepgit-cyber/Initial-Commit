import self
from locust import HttpUser, between, task
from locust.user.task import logger
from socketio.async_server import task_reference_holder


class user (HttpUser):    #first step class creation
    wait_time = between(1,5) #fixed wait time for APIs
    host = "https://test.api.hudle.in/" #Domain name (Base url) provided by dev

    @task    #decorator to  define which APis need to hit for load test
    def Testuser(self): # A function of the python
        data={
            "name": "Jdjd",
            "phone_number": "6540404044",
            "sms_channel": "1",
            "receive_updates": "1"
        }                                      #Request body data
        headers_auth = {"Api-Secret": "hudle-api1798@prod",
                        "x-app-id": "TP1A.220905.001",
                        "Content-Type": "application/json"}   #headers fixed

        with self.client.post("api/v1/register/consumer",json=data,headers=headers_auth) as response: #API http method based changes to done, client.post for Post API, same for Get and put
            if response.status_code in [200,201]:    #If command to verify reponse having status code 201 or 200 then print message
                print("API Successful") # print the details in the console of pycharm
                logger.info("API Sucessful") #Print info or message in logs of the locust
                print(response.text)
                logger.warning(response.text) #print warning in the logs of the locust whenever waring came then a excalamtion mark shown on logs of the locust
            else:
                print("API Failed")




