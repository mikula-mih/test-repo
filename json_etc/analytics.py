
import json
import time
import requests

r = requests.get('https://formulae.brew.sh/api/formula.json')
packages_json = r.json()

results = []

for package in packages_json:
    package_name = package['name']
    package_name = package['desc']
    # https://formulae.brew.sh/api/formula/a2ps.json
    package_url = f'https://formulae.brew.sh/api/formula/{package_name}.json'

    r = requests.get(package_url)
    package_json = r.json()

    package_str = json.dumps(package_json, indent=2)

    installs_30 = package_json['analytics']['install_on_request']['30d'][package_name]
    installs_90 = package_json['analytics']['install_on_request']['90d'][package_name]
    installs_365 = package_json['analytics']['install_on_request']['365d'][package_name]

    data = {
        'name': package_name,
        'desc': package_desc,
        'analytics': {
            '30d': insatlls_30,
            '90d': installs_90,
            '365d': installs_365
        }
    }

    results.append(data)

    time.sleep(r.elapsed.total_seconds())

    print(package_name, package_desc, insatlls_30, installs_90, installs_365)

with open('package_info.json', 'w') as f:
    json.dump(results, f, indent=2)

def install_sort(package):
    return package['analytics']['30d']

data = [item for item in data if 'video' in item['desc']]

data.sort(key=install_sort, reverse=True)
