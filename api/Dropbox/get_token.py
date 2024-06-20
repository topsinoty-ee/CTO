import requests
import os

APP_KEY = os.environ['DROPBOX_APP_KEY']
APP_SECRET = os.environ['DROPBOX_APP_SECRET']

auth_code = input("Enter the authorization code here: ")

url = "https://api.dropboxapi.com/oauth2/token"
data = {
    "code": auth_code,
    "grant_type": "authorization_code",
    "client_id": APP_KEY,
    "client_secret": APP_SECRET,
}

response = requests.post(url, data=data)
tokens = response.json()

if response.status_code == 200:
    print("Access Token:", tokens.get('access_token'))
    print("Refresh Token:", tokens.get('refresh_token'))
else:
    print("Error:", response.json())
