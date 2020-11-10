from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys
import glob
import pathlib
from datetime import datetime, timedelta


def get_num(pa, country, browser):
    browser.get('https://www.croxyproxy.com/')
    browser.find_element_by_id('url').send_keys("https://worldwide.espacenet.com/patent/search?f=publications.cc%3Ain%3D" + country + "&q=pa%3D%22" + pa + "%22")
    browser.find_element_by_id('requestSubmit').click()
    import time
    #time.sleep(20)
    print('Connecting to espacenet')
    while '{0} results found for' in browser.page_source:
        pass
    #import time
    #time.sleep(5)
    #print(browser.page_source)
    print('Waiting for filters')
    print(browser.page_source)
    while 'My Espacenet' not in browser.page_source:
        pass
    while True:
        try:
            for l in browser.find_elements_by_tag_name("div"):
                if l.text.endswith('results found'):
                    print(l.text)
                    return (int(l.text.replace("results found", "").replace(' ','')))
        except Exception as e:
            print(e)
            pass

def get_split(pa, country):
    options = Options()
    #options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    #options.add_argument("--mute-audio")
    options.add_experimental_option("prefs", {
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })
    browser = webdriver.Chrome(options = options)
    return [country, get_num(pa, country, browser)]
