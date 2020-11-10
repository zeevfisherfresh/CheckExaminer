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

def get_split(pa):
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
    print('Connecting to espacenet')
    browser.get("https://worldwide.espacenet.com/patent/search?q=pa%3D%22" + pa + "%22")
    while '{0} results found for' in browser.page_source:
        pass
    #import time
    #time.sleep(5)
    #print(browser.page_source)
    print('Waiting for filters')
    for l in browser.find_elements_by_tag_name("label"):
        if 'Filter' in l.text:
            l.click()
    print('Trigerring split by country')
    browser.save_screenshot("screenshot.png")
    while 'Applicants – country' not in browser.page_source:
        pass
    print('Fetching split by country')
    print(browser.page_source)
    done = False
    while not done:
        try:
            for l in browser.find_elements_by_tag_name("div"):
                if 'Applicants – country' == l.text:
                    print(l.text)
                    l.click()
                    done = True
                    break
        except Exception as e:
            print(e)
    feedback_encountered = False
    pairs = []
    for l in browser.find_elements_by_tag_name("li"):
        try:
            feedback_encountered = feedback_encountered or 'Feedback' in l.text
            if(feedback_encountered):
                pairs += [[(l.text.split('\n'))[0], int(l.text.split('\n')[1])]]
        except:
            pass
    summo = sum([i[1] for i in pairs])
    pairs = [[i[0], i[1]*1.0/summo] for i in pairs]
    browser.quit()
    return pairs
