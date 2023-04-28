import requests
import configparser

config = configparser.ConfigParser()
config.read('config.conf')

API_KEY = config.get('DEFAULT', 'API key')
ORG_ID = config.get('DEFAULT', 'Org ID')
NEW_ORG_NAME = config.get('DEFAULT', 'New Org Name')
NEW_NETWORK_NAME = config.get('DEFAULT', 'New Network Name')
TEMPLATE_NAME = config.get('DEFAULT', 'Template Name')
SERIAL_NUMBER = config.get('DEFAULT', 'serial number')
PPPOE_USERNAME = config.get('DEFAULT', 'pppoe username')
PPPOE_PASSWORD = config.get('DEFAULT', 'pppoe password')

headers = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json"
}

base_url = "https://api.meraki.com/api/v1"

# Clone organization
clone_org_url = f"{base_url}/organizations/{ORG_ID}/clone"
clone_org_data = {"name": NEW_ORG_NAME}
response = requests.post(clone_org_url, json=clone_org_data, headers=headers)
new_org_id = response.json()["id"]

# Get config templates
templates_url = f"{base_url}/organizations/{new_org_id}/configTemplates"
response = requests.get(templates_url, headers=headers)
templates = response.json()

template_network_id = None
for template in templates:
    if template["name"] == TEMPLATE_NAME:
        template_network_id = template["id"]
        break

# Create new network
create_network_url = f"{base_url}/organizations/{new_org_id}/networks"
create_network_data = {
    "name": NEW_NETWORK_NAME,
    "productTypes": ["appliance"]
}
response = requests.post(create_network_url, json=create_network_data, headers=headers)
new_network_id = response.json()["id"]

# Bind network to template
bind_network_url = f"{base_url}/networks/{new_network_id}/bind"
bind_network_data = {"configTemplateId": template_network_id}
requests.post(bind_network_url, json=bind_network_data, headers=headers)

# Unbind network from template
unbind_network_url = f"{base_url}/networks/{new_network_id}/unbind"
unbind_network_data = {"retainConfigs": True}
requests.post(unbind_network_url, json=unbind_network_data, headers=headers)

# Claim device
claim_device_url = f"{base_url}/networks/{new_network_id}/devices/claim"
claim_device_data = {"serials": [SERIAL_NUMBER]}
requests.post(claim_device_url, json=claim_device_data, headers=headers)

# Configure uplink settings
uplink_settings_url = f"{base_url}/devices/{SERIAL_NUMBER}/appliance/uplinks/settings"
uplink_settings_data = {
    "interfaces": {
        "wan1": {
            "enabled": True,
            "vlanTagging": {
                "vlanId": 1,
                "enabled": True
            },
            "pppoe": {
                "enabled": True,
                "authentication": {
                    "password": PPPOE_PASSWORD,
                    "username": PPPOE_USERNAME,
                    "enabled": True
                }
            }
        }
    }
}
requests.put(uplink_settings_url, json=uplink_settings_data, headers=headers)
