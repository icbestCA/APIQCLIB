import requests

# URL of your Flask API
api_url = 'http://127.0.0.1:5000/login'

# Username and password to send to the API
username = '012345'
password = '0000'

# Data to extract from the API
data_to_extract = ['email']

# JSON data containing the username, password, and data_to_extract
data = {'username': username, 'password': password, 'data_to_extract': data_to_extract}

# Send a POST request to the API
response = requests.post(api_url, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the JSON response
    response_data = response.json()
    for key, value in response_data.items():
        print(f"{value}")
else:
    print("Error:", response.text)
