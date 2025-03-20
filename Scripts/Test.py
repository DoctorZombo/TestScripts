import random

def LOL():
    print('Hello')
password = ''
MAX_length = 64
MIN_length = 32
ASCII = 'ABCDEFGHIKLMNOPQRSTVXYZabcdefghijklmnopqrstuvwxyz1234567890'
length = random.randint(MIN_length, MAX_length)
for i in range(length):
    password += random.choice(ASCII)
print(password)