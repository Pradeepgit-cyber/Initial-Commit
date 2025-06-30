import self
from locust import HttpUser, between, task
from locust.user.task import logger


class user(HttpUser):
    wait_time = between(1,5)
    host = "https://test.api.hudle.in/"
    phone_number = "7053355200"
    otp_code = "48353" # Replace with actual OTP retrieval if possible
    auth_token = ""

    #
    # @task(1)
    # def Learning(self):
    #
    #
    #      data = {
    #             "name": "Oppo Test ",
    #             "phone_number": "9696969696",
    #             "sms_channel": "1",
    #             "receive_updates": "1"
    #           }
    #      headers_auth ={
    # "Api-Secret": "hudle-api1798@prod",
    #             "x-app-id": "TP1A.220905.001",
    #             "Content-Type": "application/json"
    #   }
    #      with self.client.post("api/v1/register/consumer",json=data,headers=headers_auth) as response:
    #             if response.status_code in (200,201):
    #                 print("API Pass")
    #                 print(data["phone_number"])
    #
    #             else:
    #                 print("API fail")

    @task
    def otp_request_and_verify(self):
        # Step 1: Request OTP
        data_request = {
            "phone_number": self.phone_number,
            "type": "2"
        }
        headers_auth = {
            "Api-Secret": "hudle-api1798@prod",
            "x-app-id": "TP1A.220905.001",
            "Content-Type": "application/json"
        }

        with self.client.post("api/v1/otp/new", json=data_request, headers=headers_auth,
                              name="Request OTP") as response:
            if response.status_code in (200, 204):
                print("OTP Request API Pass")
            else:
                print("OTP Request API fail")
                print(response.text)
                logger.warning(response.text)
                return  # Don't proceed if OTP request failed

        # Step 2: Verify OTP
        data_verify = {
            "phone_number": self.phone_number,
            "code": self.otp_code,
            "type": "2"
        }

        with self.client.post("api/v1/otp/verify", json=data_verify, headers=headers_auth,
                              name="Verify OTP") as response:
            if response.status_code in (200, 201):
                print("OTP Verify API Pass")
                print(response.text)
                res_json = response.json()
                res_data = res_json.get("data")
                self.auth_token = res_data.get("token")
                res_json_2 = res_json.get('data',{}).get('token')
                print("test   : " f"{res_json_2}")





            else:
                print("OTP Verify API fail")
                print(response.text)
                logger.warning(response.text)

            if self.auth_token:
                headers_with_token = headers_auth.copy()
                headers_with_token["Authorization"] = f"Bearer {self.auth_token}"

                print("new headers :" f"{headers_with_token}")
                print("old headers :" f"{headers_auth}")

            else:
                print("token not found")

