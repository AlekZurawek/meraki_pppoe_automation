import requests

# Replace with your Meraki API key
MERAKI_API_KEY = "your API key goes here"

# Replace with the serial number of the Meraki device you want to retrieve the uplink settings for
DEVICE_SERIAL = "your serial goes here"

# Set the API endpoint URL
API_ENDPOINT = f"https://api.meraki.com/api/v1/devices/{DEVICE_SERIAL}/appliance/uplinks/settings"

# Set the request headers
headers = {
    "X-Cisco-Meraki-API-Key": MERAKI_API_KEY,
    "Content-Type": "application/json"
}

# Send the API request and print the response
response = requests.get(API_ENDPOINT, headers=headers)
print(response.json())
