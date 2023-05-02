# from socket import *
import requests

response = requests.get("https://ipinfo.io/json")
print(response.json())
ip = response.json()['ip']
print(response.json()['ip'])