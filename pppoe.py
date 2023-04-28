import requests
import json

# Configuration
api_key = 'your api key goes here'
base_url = 'https://api.meraki.com/api/v1'
serial = 'your serial goes here'

# Update WAN 1 settings
update_url = f'{base_url}/devices/{serial}/appliance/uplinks/settings'
update_headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json'
}
update_data = {
    'interfaces': {
        'wan1': {
            'enabled': True,
            'vlanTagging': {
                'vlanId': 1,
                'enabled': True
            },
            'pppoe': {
                'enabled': True,
                'authentication': {
                    'password': 'your PPPoE password goes here',
                    'username': 'your PPPoE username goes here',
                    'enabled': True
                }
            }
        }
    }
}

response = requests.put(update_url, headers=update_headers, data=json.dumps(update_data))
response.raise_for_status()

# Retrieve and print updated WAN settings
get_url = f'{base_url}/devices/{serial}/appliance/uplinks/settings'
get_headers = {
    'X-Cisco-Meraki-API-Key': api_key
}

response = requests.get(get_url, headers=get_headers)
response.raise_for_status()
settings = response.json()

print(json.dumps(settings, indent=2))
