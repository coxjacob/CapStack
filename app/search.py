from typing import Any, List
from pathlib import Path

import curl_cffi   # used for requesting data from web pages
from bs4 import BeautifulSoup as bs  #used to pard web page data
import json
import re



#r = curl_cffi.get("https://tls.browserleaks.com/json", impersonate="chrome")
#print(r.json())

# Extract address information from Zillow
def retrieve_data(target_url: str, address: str) -> str:
    r = curl_cffi.get(target_url + address, impersonate="chrome", headers={"Accept-Language": "en-US,en;q=0.9"})
    #r = curl_cffi.get(r"https://www.zillow.com/homedetails/3840-Boulder-Creek-Rd-Martinez-GA-30907/83373999_zpid/",
    #                   impersonate="chrome", headers={"Accept-Language": "en-US,en;q=0.9"})
    return r.text

def write_to_file(data: str, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data written to {filename}")

def parse_days_saves(data: str) -> List[Any]:
    days = re.search(r'(\d+)\s+dayson', data)
    saves = re.search(r'(\d+)\s*saves', data)
    return [days.group(1) if days else None, saves.group(1) if saves else None]

if __name__ == "__main__":
    if not Path("data.txt").is_file():
        print("File not found, retrieving data...")
        #address = "3840-Boulder-Creek-Rd-Martinez-GA-30907/83373999_zpid/"
        address = "161-Hickory-Dr-S-Martinez-GA-30907/14209886_zpid/"
        target_url = "https://www.zillow.com/homedetails/"
        raw_text = retrieve_data(target_url, address)
        print(type(raw_text))
        with open("data.txt", 'w') as f:
            f.write(raw_text)
    else:
        print("File found, reading data...")
        with open("data.txt", 'r') as f:
            raw_text = f.read()
    
    soup = bs(raw_text, 'html.parser')
    zillow_data = {}

    # Collect Zestimate Value
    zestimate = soup.find_all('div', {'class':["styles__StyledPriceAndBathWrapper-fshdp-8-111-1__sc-ncazb7-1 jCFmeF",
                                               "Text-c11n-8-111-1__sc-aiai24-0 sc-hAQmFe bzMbAh dcvJrC"]})
    print(type(zestimate))
    for z in zestimate:
        zillow_data.setdefault('zestimate', z.text)

    # Collect days on market and saves
    days = soup.find_all('dl', {'class':'styles__StyledOverviewStats-fshdp-8-111-1__sc-1x11gd9-0 kpgmGL'})
    for day in days:
        print(day.text)
        days_saves = parse_days_saves(day.text)
        zillow_data.setdefault('days', days_saves[0]) 
        zillow_data.setdefault('saves', days_saves[1])

    print("Geting years")
    years = soup.find_all('div', {'class':"styles__StyledCategories-fshdp-8-111-1__sc-1mj0p8k-0 fJbWJL"})
    for year in years:
        print(year.text)
    print("Missed it")
    # Get beds
    beds = soup.find_all('span', {'class':"Text-c11n-8-111-1__sc-aiai24-0 StyledHeading-c11n-8-111-1__sc-s7fcif-0 gqVRdW styles__StyledFactCategoryHeading-fshdp-8-111-1__sc-1i5yjpk-2 dqRTUj"})
    for bed in beds: 
        zillow_data.setdefault('beds', bed.text)



    print(zillow_data)