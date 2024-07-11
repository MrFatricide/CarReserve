import requests
import json

# Define the URL to send the POST request to
url = "http://127.0.0.1:5000/signup"

# Define the JSON payload to send in the request
payload = {
    "username": "test3",
    "email": "email3@gmail.com",
    "password": "password123"
}

# Convert the payload to JSON format
json_payload = json.dumps(payload)

# Set the headers for the request
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, data=json_payload, headers=headers)

# Check the response status code
if response.status_code == 200:
    print(response.text)
else:
    print(response.text)