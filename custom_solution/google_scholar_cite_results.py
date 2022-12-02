from parsel import Selector
import requests, json, os

# requestHandler()
import random

# selenijm_stealth
from selenium import webdriver
from selenium_stealth import stealth
import time

import sys
sys.path.append("..")
from app import requestHandler

"""
python3 -m google_scholar_cite_results.py
"""

params = {
    "q": "microservice", # search query
    "hl": "en"       # language of the search   
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    'accept-language': 'en-US,en',
    "referer": f"https://scholar.google.com/scholar?hl={params['hl']}&q={params['q']}"
}


def parsel_get_cite_ids():
    print("parsel_get_cite_ids()")
    URL = "https://scholar.google.com/scholar"
    #html = requests.get(URL, params=params, headers=headers)
    webdriver = requestHandler(URL,params)
    print(webdriver.page_source)
    #soup = Selector(text=html.text)
    soup = Selector(text=webdriver.page_source)

    # returns a list of publication ID's -> U8bh6Ca9uwQJ
    return soup.css(".gs_r.gs_or.gs_scl::attr(data-cid)").getall()


def parsel_scrape_cite_results():
    citations = []
    cite_id_example = [[1.00113E+19],[1.73226E+19],[1.30399E+19],[7.17069E+17]]
    print("parsel_scrape_cite_results()")

    for cite_id in parsel_get_cite_ids():
        print(cite_id)
        html = requests.get(f"https://scholar.google.com/scholar?output=cite&q=info:{cite_id}:scholar.google.com", headers=headers)
        selector = Selector(text=html.text)
         
        # might be issues in the future with extracting data from the table
        if selector.css('#gs_citt').get():
            for result in selector.css("tr"):
                institution = result.xpath("th/text()").get()
                citation = result.xpath("td div/text()").get()

                citations.append({"institution": institution, "citations": citation})

    return citations



if __name__ == "__main__":
    sys.path.append("..")
    print(parsel_get_cite_ids())


