import requests
from util.constants import FOURSQUAREKEY

url = "https://api.foursquare.com/v3/places/search"

headers = {
    "accept": "application/json",
    "Authorization": FOURSQUAREKEY
}


response = requests.get(url, headers=headers)

print(response.text)