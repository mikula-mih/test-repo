import requests
proxies = {
    'https': 'https://52.183.8.192:3128',
    'https': 'https://140.227.69.170:6000'
}

'''Shows your IPm location & ISP
'''
response = requests.get("https://ipinfo.io/json")
print(response.json())

response = requests.get("https://ipinfo.io/json", proxies=proxies)
print(response.json())
print(response.json()['country'])