from typing import Any, List
from pathlib import Path

import curl_cffi   # used for requesting data from web pages
from bs4 import BeautifulSoup as bs  #used to pard web page data
import json
import re
import logging


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def retrieve_data(target_url: str) -> list:
    """Returns status and data"""
    r = curl_cffi.get(target_url, 
                      impersonate="chrome", 
                      headers={"Accept-Language": "en-US,en;q=0.9"})
    status = r.status_code
    logging.info(f"HTTP Status Code: {status}")
    print(status)
    if status != 200:
        return ["Error", ""]
    else:
        return ["OK", r.text]

def write_to_file(data: str, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data written to {filename}")



if __name__ == "__main__":
    target_url = "https://www.metoc.navy.mil/fwcsd/fwc-sd.html"
    # Create filename from URL
    filename = target_url.split("//")[-1].replace(".", "").replace('/','-') 
    filename = filename.replace('www', '').replace('html','') + '.txt'
    file_exists = Path(filename).is_file()

    if not file_exists:
        print("File not found, retrieving data...")
        stat, raw_text = retrieve_data(target_url)
        if stat == "OK":
            with open(filename, 'w') as f:
                f.write(raw_text)
    else:
        print("File found, reading data...")
        with open("data.txt", 'r') as f:
            raw_text = f.read()


    if raw_text != "":  
        soup = bs(raw_text, 'html.parser')
        # title = soup.find('title').get_text()
        # print(title)
        information = soup.find_all('div', attrs={'class': 'page-content'})
        #for info in information:
           #print(info.get_text())
        links = soup.find_all('a')
        emails = []
        add_urls = []
        for link in links:
            href = link.get('href')
            if href not in [None, "#"]:
                if 'mailto:' in href:
                    emails.append(href.split(':')[1])
                else:
                    add_urls.append(link.get('href'))
        print("Email addresses found:", emails)
        print("Additional URLs found:", add_urls)

