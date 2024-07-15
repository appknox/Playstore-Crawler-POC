import requests

try:
    response = requests.get('https://play.google.com', verify=True)
    response.raise_for_status()
    print('Connection successful:', response.status_code)
except requests.exceptions.RequestException as e:
    print('Connection error:', e)