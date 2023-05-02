""" JavaScript Object Notation """
import json

people_string = '''
{
    "people": [
        {
            "name": "Mike-0",
            "phone": "000-000-0000",
            "emails": ["mike@mike.com", "default@mike.com"],
            "has_license": false
        },
        {
            "name": "Mike-1",
            "phone": "111-111-1111",
            "emails": null,
            "has_license": true
        }
    ]
}
'''

data = json.loads(people_string) # json.loads() - for string

print(type(data))
print(type(data['people']))
print(data)

for person in date['people']:
    print(person['name'])
    del person['phone']

new_string = json.dumps(data, indent=2, sort_keys=True)
print(new_string)

#####
with open('states.json') as f:
    data = json.load(f) # json.load() - for files

for state in data['states']:
    print(state['name'], state['abbreviation'])
    del state['area_codes']

with open('new_states.json', 'w') as f:
    json.dump(data, f, indent=2)

####
from urllib.request import urlopen

with urlopen("https://finance.yahoo.com/webservice/v1/symbols/\
            allcurrencies/quote?format=json") as response:
    source = response.read()

data = json.loads(source)

for item in data['list']['resources']:
    name = item['resource']['fields']['name']
    price = item['resource']['fields']['price']
    usd_rates[name] = price

print(50 * float(usd_rates['USD/INR']))
