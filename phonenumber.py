import random
import string


def generate_phone_number():
    return str( random.randint(6, 9)) + ''.join(random.choices(string.digits, k=9))



test = generate_phone_number()

print("+91" + test)