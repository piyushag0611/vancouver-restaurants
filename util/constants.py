import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

YELPKEY = parser.get(section='api_keys', option='yelp_api_key')
FOURSQUAREKEY = parser.get(section='api_keys', option='foursquare_api_key')



