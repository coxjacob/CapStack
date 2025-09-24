from typing import Any, List
from pathlib import Path

import curl_cffi   # used for requesting data from web pages
import json
import re
import logging

from bs4 import BeautifulSoup as bs  #used to pard web page data
#import lxml import etree could not get etree to be recognized 


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_filename(url: str) -> str:
    "Use URL to create unique file name."
    filename = url.split('//')[-1].replace('.','-').replace('/','-') + ".txt"
    logging.info(f"Created file: {filename}")
    return filename

def retrieve_data(target_url: str) -> list:
    "Obtain raw text and dat from URL"
    r = curl_cffi.get(target_url, 
                      impersonate="chrome", 
                      headers={"Accept-Language": "en-US,en;q=0.9"})
    status = r.status_code
    logging.info(f"HTTP Status Code: {status}")
    return [status, r.text]

def get_url_raw_text(filename: str, target_url: str) -> str:
    "Extract raw text from URL if first use or file if subsequent use"
    logging.info(f"Getting raw text from {filename} or {target_url}")
    if not Path(filename).is_file():
        print("File not found, retrieving data...")
        stat, raw_text = retrieve_data(target_url)
        if stat == 200:
            logging.info(f"Writing to file: {filename}")
            with open(filename, 'w') as f:  # Write content to file for further work and testing
                f.write(raw_text)
        else:
            raw_text = "" #don't bother sending data if status not okay
    else:
        print("File found, reading data...")
        with open(filename, 'r') as f:
            raw_text = f.read()    
    return raw_text


if __name__ == "__main__":
    target_search = "submarine+russian"
    #url = "https://search.usa.gov/search?affiliate=defense_gov&query=submarine"
    url = f"https://search.usa.gov/search?affiliate=defense_gov&sort_by=&query={target_search}"
    print (url)
    filename = create_filename(str(url))
    raw_text = get_url_raw_text(filename, url)
    
    if raw_text != "": 
        #print(raw_text[:300])
        soup = bs(raw_text, "html.parser")
        target_divs = soup.find_all('div', class_='content-block-item result')
        if target_divs:
            count = 0
            for target_div in target_divs:
                print(f"Number {count}: ")
                links = target_div.find_all('a')
                for link in links:
                    href = link.get('href')
                    h_name = link.get_text()
                
                div_text = target_div.get_text(separator=" ", strip=True)
                if 'submarin' in div_text:
                    print(div_text)
                    print(f"Link: {h_name} - {href} ")
                    # print these to a JSON
                    # Let's let an LLM intuit whether the title or text indicates we should read more about the file 
                print()
                count +=1
        #print(matches)
    else:
        print("No text")
 
