from typing import Any, List

import curl_cffi
from bs4 import BeautifulSoup as bs

#from curl_cffi import requests
import json

address = "3840-Boulder-Creek-Rd-Martinez-GA-30907/"
url = "https://www.zillow.com/homedetails/"

#r = curl_cffi.get("https://tls.browserleaks.com/json", impersonate="chrome")
#print(r.json())

# Extract address information from Zillow
r = curl_cffi.get(url+address, impersonate="chrome")

soup = bs(r.text, 'html.parser')


#print(soup.extract())
print(soup.find_all('text'))

