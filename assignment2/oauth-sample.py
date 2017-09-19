import requests
import base64
import json

# Example: Twitter API "Application-only authentication"
# Reference: https://dev.twitter.com/oauth/application-only

consumer_key = your_consumer_key_here
consumer_secret = your_consumer_secret_here

# Step 1: Encode consumer key and secret
credentials = base64.b64encode(consumer_key + ':' + consumer_secret)

# Step 2: Obtain a bearer token
payload = { 'grant_type': 'client_credentials' }
headers = { 'Authorization': 'Basic ' + credentials, 
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }

r = requests.post("https://api.twitter.com/oauth2/token", 
                  headers=headers, data=payload)

# Response is JSON data. Decode and display the access token
j = json.loads(r.content)
print 'Access token:', j['access_token']

# Step 3: Authenticate API requests with the bearer token
