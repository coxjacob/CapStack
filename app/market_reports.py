from typing import Any, List
from pathlib import Path

import curl_cffi   # used for requesting data from web pages
from bs4 import BeautifulSoup as bs  #used to pard web page data
import json
import re


def retrieve_data(target_url: str) -> list:
    r = curl_cffi.get(target_url, impersonate="chrome", headers={"Accept-Language": "en-US,en;q=0.9"})
    status = r.status_code
    print(status)
    if status != 200:
        return ["Error", ""]
    else:
        return ["OK", r.text]

def write_to_file(data: str, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data written to {filename}")

def get_url_data(filename: str, target_url: str) -> str:
    if not Path(filename).is_file():
        print("File not found, retrieving data...")
        stat, raw_text = retrieve_data(target_url)
        if stat == "OK":
            print(type(raw_text))
            with open(filename, 'w') as f:
                f.write(raw_text)
    else:
        print("File found, reading data...")
        with open(filename, 'r') as f:
            raw_text = f.read()    
    return raw_text

if __name__ == "__main__":
    url = "https://www.marketsandmarkets.com/Market-Reports/sonobuoy-market-114611169.html"
    filename = "market_report2.html"
    raw_text = get_url_data(filename, url)
    if raw_text != "": 
        hits = re.findall(r'align="justify"(.+?)<.p>', raw_text, re.I|re.DOTALL)
        print(f"Found {len(hits)} hits")
        for hit in hits:
            if "strong" not in hit:
                print(hit.strip())













