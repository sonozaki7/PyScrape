"""
source ~/desktop/project/pyscrapeEnv/bin/activate

sudo xcode-select --switch /Applications/Xcode.app
/Applications/Xcode.app

python3 app.py
"""

from bs4 import BeautifulSoup
import requests, lxml, os, json
from parsel import Selector

# requestHandler()
import random

# selenium_stealth
from selenium import webdriver
from selenium_stealth import stealth
import time

# Proxy Rotation
from fp.fp import FreeProxy

# For CSV parsing
import pandas

# For filtering venue names
import re

# For selenium web scrape tutorial
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import org.openqa.selenium.support.ui.Select;
from selenium.webdriver.support.select import Select
#import org.openqa.selenium.By;


def scrape_one_google_scholar_page():
    # https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    # https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    params = {
        'q': 'microservices',  # search query
        'hl': 'en'       # language of the search
    }
    html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
    soup = BeautifulSoup(html, 'lxml')
    # JSON data will be collected here
    data = []
    # Container where all needed data is located
    for result in soup.select('.gs_r.gs_or.gs_scl'):
        title = result.select_one('.gs_rt').text
        title_link = result.select_one('.gs_rt a')['href']
        publication_info = result.select_one('.gs_a').text
        snippet = result.select_one('.gs_rs').text
        cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
        #"""
        related_articles_URL = result.select_one('a:nth-child(4)')['href']
        related_articles_txt = result.select_one('a:nth-child(4)').text
        all_article_versions_URL = result.select_one('.gs_nph:nth-child(5)')['href']
        all_article_versions_txt = result.select_one('.gs_nph:nth-child(5)').text
        #"""
        try:
            pdf_link = result.select_one('.gs_or_ggsm a:nth-child(1)')['href']
        except: 
            pdf_link = None
            data.append({
            'title': title,
            'title_link': title_link,
            'publication_info': publication_info,
            'snippet': snippet,
            'cited_by': f'https://scholar.google.com{cited_by}',
            #"""

            'related_articles_URL': f'https://scholar.google.com{related_articles_URL}',
            #a:nth-child(4)
            'all_article_versions_URL': f'https://scholar.google.com{all_article_versions_URL}',
            'all_article_versions_txt': all_article_versions_txt,
            #.gs_nph:nth-child(5)

            #"""

            "pdf_link": pdf_link
        })
        print(data)
        print(json.dumps(data, indent = 2, ensure_ascii = False))
        # Part of the JSON Output:
    '''
    [
    {
        "title": "“What? I thought Samsung was Japanese”: accurate or not, perceived country of origin matters",
        "title_link": "https://www.emerald.com/insight/content/doi/10.1108/02651331111167589/full/html",
        "publication_info": "P Magnusson, SA Westjohn… - International Marketing …, 2011 - emerald.com",
        "snippet": "Purpose–Extensive research has shown that country‐of‐origin (COO) information significantly affects product evaluations and buying behavior. Yet recently, a competing perspective has emerged suggesting that COO effects have been inflated in prior research …",
        "cited_by": "https://scholar.google.com/scholar?cites=341074171610121811&as_sdt=2005&sciodt=0,5&hl=en",
        "related_articles": "https://scholar.google.com/scholar?q=related:U8bh6Ca9uwQJ:scholar.google.com/&scioq=samsung&hl=en&as_sdt=0,5",
        "all_article_versions": "https://scholar.google.com/scholar?cluster=341074171610121811&hl=en&as_sdt=0,5"
    }
    ]
    '''


def google_scholar_pagination():
    # https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    # https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    params = {
        'q': 'samsung medical center seoul semiconductor element simulation x-ray fetch',
        'hl': 'en',       # language of the search
        'start': 0        # page number ⚠
    }
    # JSON data will be collected here
    data = []
    while True:
        html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
        selector = Selector(text=html)
        print(f'extrecting {params["start"] + 10} page...')
        # Container where all needed data is located
        for result in selector.css('.gs_r.gs_or.gs_scl'):
            title = result.css('.gs_rt').xpath('normalize-space()').get()
            title_link = result.css('.gs_rt a::attr(href)').get()
            publication_info = result.css('.gs_a').xpath('normalize-space()').get()
            snippet = result.css('.gs_rs').xpath('normalize-space()').get()
            cited_by_link = result.css('.gs_or_btn.gs_nph+ a::attr(href)').get()
            data.append({
                'page_num': params['start'] + 10, # 0 -> 1 page. 70 in the output = 7th page
                'title': title,
                'title_link': title_link,
                'publication_info': publication_info,
                'snippet': snippet,
                'cited_by_link': f'https://scholar.google.com{cited_by_link}',
            })
        # check if the "next" button is present
        if selector.css('.gs_ico_nav_next').get():
            params['start'] += 10
        else:
            break
        print(json.dumps(data, indent = 2, ensure_ascii = False))
        google_scholar_pagination()

        # Part of the output:
        '''
        extrecting 10 page...
        extrecting 20 page...
        extrecting 30 page...
        extrecting 40 page...
        extrecting 50 page...
        extrecting 60 page...
        extrecting 70 page...
        extrecting 80 page...
        extrecting 90 page...
        [
        {
            "page_num": 10,
            "title": "Comparative analysis of root canal filling debris and smear layer removal efficacy using various root canal activation systems during endodontic retreatment",
            "title_link": "https://www.mdpi.com/891414",
            "publication_info": "SY Park, MK Kang, HW Choi, WJ Shon - Medicina, 2020 - mdpi.com",
            "snippet": "… According to a recent study, the GentleWave System was effective in retrieving separated … Energy dispersive X-ray spectroscopy (EDX) may be used for the microchemical analysis of …",
            "cited_by_link": "https://scholar.google.com/scholar?cites=5221326408196954356&as_sdt=2005&sciodt=0,5&hl=en"
        },
        {
            "page_num": 90,
            "title": "Αυτόματη δημιουργία ερωτήσεων/ασκήσεων για εκπαιδευτικό σύστημα διδασκαλίας τεχνητής νοημοσύνης",
            "title_link": "http://nemertes.lis.upatras.gr/jspui/handle/10889/9424",
            "publication_info": "Ν Νταλιακούρας - 2016 - nemertes.lis.upatras.gr",
            "snippet": "Στόχος της διπλωματικής είναι ο σχεδιασμός ,η ανάπτυξη και υλοποίηση ενός συστήματος παραγωγής ερωτήσεων/ασκήσεων από κείμενα φυσικής γλώσσας. Κύριος στόχος των …",
            "cited_by_link": "https://scholar.google.com/scholar?q=related:1ovrKI-7xtUJ:scholar.google.com/&scioq=samsung+medical+center+seoul+semiconductor+element+simulation+x-ray+fetch&hl=en&as_sdt=0,5",
        }
        ]
        '''

def requestHandler(URL,params):
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    #Pick a random user agent
    user_agent_chosen = random.randint(0,4)
    #Set the headers 
    headers = {'User-Agent': user_agent_list[user_agent_chosen]}
    print("Agent " + str(user_agent_chosen) + " is chosen")
        
    # selenium_stealth code
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    # Get a newest proxy server that responds within 1 second
    proxy = FreeProxy(timeout=4).get()
    options.add_argument(f'--proxy-server={proxy}')
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #Webdriver = webdriver.Chrome(options=options, executable_path=r"/Users/so/Desktop/Project/ChromeDriverDir/chromedriver")
    Webdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    """ stealth(driverVar,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            ) """
    
    stealth(
        Webdriver,
        user_agent_list[user_agent_chosen],
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=False,
        )

    #url = "https://bot.sannysoft.com/"
    Webdriver.get(URL)
    #time.sleep(10)
    #Webdriver.quit()

    #return requests.get(URL, headers=headers, params=params)
    return Webdriver



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
    #URL_checks = "https://bot.sannysoft.com/"
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

def findVenueRank(conf, mimicReal):
    if conf:
        df = pandas.read_excel('venue.xlsx')
    else:
        df = pandas.read_excel('venue_scraped.xlsx')

    if conf:
        thesisType = "conf_"
    else: 
        thesisType = "journal_"

    # Reset the 1st index column created when writing to the file twice
    df.reset_index(drop=True, inplace=True)

    type_select = '#searchform > select:nth-child(2)'
    year_select = '#searchform > select:nth-child(3)'
    search_select = '#searchform > input[type=text]:nth-child(1)'
    result_title_select = '#search > table > tbody > tr.evenrow > td:nth-child(1)'
    result_rank_select = '#search > table > tbody > tr.evenrow > td:nth-child(4)'
    n = 2
    nth_result_title_select = "#search > table > tbody > tr:nth-child(" + str(n) + ") > td:nth-child(1)"
    nth_result_rank_select = "#search > table > tbody > tr:nth-child(" + str(n) + ") > td:nth-child(4)"

    search_button = '#searchform > input[type=submit]:nth-child(7)'
    
    if conf:
        URL = 'http://portal.core.edu.au/conf-ranks/'
    else:
        URL = 'http://portal.core.edu.au/jnl-ranks/'

    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(
        options=options,
    )

    if mimicReal:
        browser.get(URL)
    else:
        params = 0
        browser = requestHandler(URL, params)

    dropDown = Select(browser.find_element(By.CSS_SELECTOR, type_select)).select_by_visible_text('Title')
    dropDown = Select(browser.find_element(By.CSS_SELECTOR, year_select)).select_by_visible_text('All')
    for i in range(len(df["venue"])):
        print("iteration at index " + str(i))

        print("data at index " + str(i) + " = " + str(df.at[i,"venue"]))
        if str(df.at[i,"venue"]) == "nan" :
            print("the str value at index " + str(i) + " was 'nan' ")
            continue

        browser.find_element(
            By.CSS_SELECTOR, search_select).send_keys(df.at[i,"venue"])
        
        browser.find_element(
            By.CSS_SELECTOR, search_button).click()
        

        #WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, result_title_select)))
        name_column = thesisType + "result_name"
        rank_column = thesisType + "result_rank"
        if browser.find_elements(By.CSS_SELECTOR, result_title_select) and browser.find_elements(By.CSS_SELECTOR, result_rank_select):

            num_result = browser.find_elements(By.XPATH, ("//*[contains(text(),'Showing results ')]"))
            if len(num_result) > 0:
                num_result = num_result[0].text
            print("num_result = " + str(num_result))

            n = 2
            print("n = " + str(n))
            nth_result_title_select = "#search > table > tbody > tr:nth-child(" + str(n) + ") > td:nth-child(1)"
            if conf:
                nth_result_rank_select = "#search > table > tbody > tr:nth-child(" + str(n) + ") > td:nth-child(4)"
            else:
                nth_result_rank_select = "#search > table > tbody > tr:nth-child(" + str(n) + ") > td:nth-child(3)"

            title = browser.find_elements(By.CSS_SELECTOR, nth_result_title_select)
            if len(title) > 0:
                df.at[i,name_column] = title[0].text
                print(title[0].text)
            
            rank = browser.find_elements(By.CSS_SELECTOR, nth_result_rank_select)
            if len(rank) > 0:
                df.at[i,rank_column] = rank[0].text
                print(rank[0].text + "\n")
            #df.to_excel('venue_scraped.xlsx')

        browser.find_element(
            By.CSS_SELECTOR, search_select).clear()

        
        

        
        """ password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"

        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

        browser.find_element(
            By.CSS_SELECTOR, password_selector).send_keys(password)

        browser.find_element(
            By.CSS_SELECTOR, '#passwordNext > div > button > span').click() """

def preFiltering():
    df = pandas.read_excel('venue.xlsx')
    words = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']
    for i in range(len(df["venue"])):
        for w in words:
            df.at[i,"venue"] = re.sub(r' \b%s\b ' % w, '', str(df.at[i,"venue"]))  # '\b' is a word boundry
            df.at[i,"venue"] = re.sub(r'\b%s\b ' % w, '', str(df.at[i,"venue"]))  # '\b' is a word boundry
            df.at[i,"venue"] = re.sub(r' \b%s\b' % w, '', str(df.at[i,"venue"]))  # '\b' is a word boundry
            df.at[i,"venue"] = re.sub(r'\b%s\b' % w, '', str(df.at[i,"venue"]))  # '\b' is a word boundry

        df.to_excel('venue.xlsx')
        
        if i % 100 == 0:
            print("iteration = " + str(i))
            print(df['venue'])

    print(df['venue'])

    return True

    
if __name__ == "__main__":
    """ print("function 1")
    scrape_one_google_scholar_page()
    print("function 2")
    google_scholar_pagination()
    
    print(parsel_get_cite_ids())
    print(parsel_scrape_cite_results()) """

    preFiltering()
    mimicReal = True
    findVenueRank(True,mimicReal)
    mimicReal = True
    findVenueRank(False,mimicReal)

