import random
import string


def generate_phone_number():
    return str( random.randint(6, 9)) + ''.join(random.choices(string.digits, k=9))



test = generate_phone_number()

print("+91" + test)

headers_auth = {
    "Api-Secret": "hudle-api1798@prod",
    "x-app-id": "TP1A.220905.001",
    "Content-Type": "application/json",
    "nekje": "dhbkhe",
    "Chirag":"Pradeep"
}


def testing(self):
    header_with_Authtoken = headers_auth.copy()
    return header_with_Authtoken


