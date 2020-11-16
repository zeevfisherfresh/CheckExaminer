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

def ipc(classi):
    import requests

    cookies = {
        'cpcops_settings': '%7B%22display_tree%22%3Atrue%2C%22show-2000-series%22%3A%22state-1%22%2C%22dateRange%22%3A%7B%22from%22%3A%7B%22month%22%3A10%2C%22year%22%3A2020%7D%2C%22to%22%3A%7B%22month%22%3A10%2C%22year%22%3A2020%7D%2C%22isRange%22%3Afalse%7D%7D',
        'cart': '%5B%5D',
        'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE': 'en_EP',
        'LevelXLastSelectedDataSource': 'EPODOC',
        'splashPopup': '2020-06-30',
        'menuCurrentSearch': '%2F%2Fworldwide.espacenet.com%2FsearchResults%3FAB%3D%26AP%3D%26CPC%3D%26DB%3DEPODOC%26IC%3D%26IN%3D%26PA%3DIBM%26PD%3D%26PN%3D%26PR%3D%26ST%3Dadvanced%26Submit%3DSearch%26TI%3D%26locale%3Den_EP',
        'PGS': '10',
        'currentUrl': 'https%3A%2F%2Fworldwide.espacenet.com%2FadvancedSearch%3Flocale%3Den_EP',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
        'Accept': 'application/json,application/i18n+xml',
        'X-EPO-PQL-Profile': 'cpci',
        'EPO-Trace-Id': 'a0ryb7-s9wjrp-AAA-000025',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://worldwide.espacenet.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://worldwide.espacenet.com/patent/search?q='+classi,
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    params = (
        ('lang', 'en,de,fr'),
        ('q', 'ipc="' + classi +'"'),
        ('qlang', 'cql'),
        ('p_s', 'espacenet'),
        ('widgets', ''),
        ('p_q', 'ipc="' + classi + '"'),
    )

    data = '{"query":{"fields":["publications.ti_*","publications.abs_*","publications.pn_docdb","publications.in","publications.in_country","publications.pa","publications.pa_country","publications.pd","publications.pr_docdb","publications.app_fdate.untouched","publications.ipc","publications.ipc_ic","publications.ipc_icci","publications.ipc_iccn","publications.ipc_icai","publications.ipc_ican","publications.ci_cpci","publications.ca_cpci","publications.cl_cpci","biblio:pa;pa_orig;pa_unstd;in;in_orig;in_unstd;pa_country;in_country;pd;pn;allKindCodes;","oprid_full.untouched","opubd_full.untouched"],"from":0,"size":1,"highlighting":[{"field":"publications.ti_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.ti_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.ti_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pn","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pn_docdb","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pa","fragment_words_number":20,"number_of_fragments":3,"hits_only":true}]},"filters":{"publications.patent":[{"value":["true"]}]},"widgets":{"pa_full":{"size":100,"weighted":false},"cc":{"size":100,"weighted":false},"publications.cc":{"size":100,"weighted":false},"cpc_cpci_main":{"size":100,"weighted":false},"cpc_cpci_full":{"size":150,"weighted":false},"ci_ca_cpci_cc":{"size":100,"weighted":false},"ipc_main":{"size":100,"weighted":false},"ipc_full":{"size":150,"weighted":false},"in_full":{"size":100,"weighted":false},"lang":{"size":100},"publications.lang":{"size":100},"pd":{"type":"date_histogram","interval":"year","field":"pd"},"publications.pd":{"type":"date_histogram","interval":"year","field":"publications.pd"},"oprid":{"type":"date_histogram","interval":"year","field":"oprid"},"publications.pa_country":{"size":100,"weighted":false},"publications.in_country":{"size":100,"weighted":false}}}'

    response = requests.post('https://worldwide.espacenet.com/3.2/rest-services/search', headers=headers, params=params, cookies=cookies, data=data)
    return response.json()
def temp(patent):
    import requests

    cookies = {
        'cpcops_settings': '%7B%22display_tree%22%3Atrue%2C%22show-2000-series%22%3A%22state-1%22%2C%22dateRange%22%3A%7B%22from%22%3A%7B%22month%22%3A10%2C%22year%22%3A2020%7D%2C%22to%22%3A%7B%22month%22%3A10%2C%22year%22%3A2020%7D%2C%22isRange%22%3Afalse%7D%7D',
        'cart': '%5B%5D',
        'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE': 'en_EP',
        'LevelXLastSelectedDataSource': 'EPODOC',
        'splashPopup': '2020-06-30',
        'menuCurrentSearch': '%2F%2Fworldwide.espacenet.com%2FsearchResults%3FAB%3D%26AP%3D%26CPC%3D%26DB%3DEPODOC%26IC%3D%26IN%3D%26PA%3DIBM%26PD%3D%26PN%3D%26PR%3D%26ST%3Dadvanced%26Submit%3DSearch%26TI%3D%26locale%3Den_EP',
        'PGS': '10',
        'currentUrl': 'https%3A%2F%2Fworldwide.espacenet.com%2FadvancedSearch%3Flocale%3Den_EP',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
        'Accept': 'application/json,application/i18n+xml',
        'X-EPO-PQL-Profile': 'cpci',
        'EPO-Trace-Id': 'a0ryb7-s9wjrp-AAA-000025',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://worldwide.espacenet.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://worldwide.espacenet.com/patent/search?q='+patent,
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    params = (
        ('lang', 'en,de,fr'),
        ('q', 'pa="' + patent +'"'),
        ('qlang', 'cql'),
        ('p_s', 'espacenet'),
        ('widgets', ''),
        ('p_q', 'pa="' + patent + '"'),
    )

    data = '{"query":{"fields":["publications.ti_*","publications.abs_*","publications.pn_docdb","publications.in","publications.in_country","publications.pa","publications.pa_country","publications.pd","publications.pr_docdb","publications.app_fdate.untouched","publications.ipc","publications.ipc_ic","publications.ipc_icci","publications.ipc_iccn","publications.ipc_icai","publications.ipc_ican","publications.ci_cpci","publications.ca_cpci","publications.cl_cpci","biblio:pa;pa_orig;pa_unstd;in;in_orig;in_unstd;pa_country;in_country;pd;pn;allKindCodes;","oprid_full.untouched","opubd_full.untouched"],"from":0,"size":1,"highlighting":[{"field":"publications.ti_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.ti_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.ti_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pn","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pn_docdb","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pa","fragment_words_number":20,"number_of_fragments":3,"hits_only":true}]},"filters":{"publications.patent":[{"value":["true"]}]},"widgets":{"pa_full":{"size":100,"weighted":false},"cc":{"size":100,"weighted":false},"publications.cc":{"size":100,"weighted":false},"cpc_cpci_main":{"size":100,"weighted":false},"cpc_cpci_full":{"size":150,"weighted":false},"ci_ca_cpci_cc":{"size":100,"weighted":false},"ipc_main":{"size":100,"weighted":false},"ipc_full":{"size":150,"weighted":false},"in_full":{"size":100,"weighted":false},"lang":{"size":100},"publications.lang":{"size":100},"pd":{"type":"date_histogram","interval":"year","field":"pd"},"publications.pd":{"type":"date_histogram","interval":"year","field":"publications.pd"},"oprid":{"type":"date_histogram","interval":"year","field":"oprid"},"publications.pa_country":{"size":100,"weighted":false},"publications.in_country":{"size":100,"weighted":false}}}'

    response = requests.post('https://worldwide.espacenet.com/3.2/rest-services/search', headers=headers, params=params, cookies=cookies, data=data)
    return response.json()

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.post('https://worldwide.espacenet.com/3.2/rest-services/search?lang=en%2Cde%2Cfr&q=THE%20CHERTOFF%20GROUP&qlang=cql&p_s=espacenet&widgets&p_q=THE%20CHERTOFF%20GROUP', headers=headers, cookies=cookies, data=data)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://worldwide.espacenet.com/3.2/rest-services/search?lang=en%2Cde%2Cfr&q=pa%3D%22IBM%22&qlang=cql&p_s=espacenet&p_f=publications.pa_country%3Ain%3Dgb&p_q=pa%3D%22IBM%22', headers=headers, cookies=cookies, data=data)


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

def get_class_text(cl):
    import requests
    print('Fetching info about class', cl)
    headers = {
        'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
        'Accept': '*/*',
        'Referer': 'https://worldwide.espacenet.com/patent/static/cpc.html',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    }

    params = (
        ('depth', '0'),
        ('interleave', ''),
        ('ancestors', ''),
        ('navigation', ''),
        ('origin', 'https_worldwide_espacenet_com'),
    )

    resp = response = requests.get('https://worldwide.espacenet.com/3.2/rest-services/classification/cpc/' + cl + '.json', headers=headers, params=params).json()
    resp = resp['ops:world-patent-data']['ops:classification-scheme']['ops:cpc']['cpc:class-scheme']
    while 'cpc:classification-item' in resp:
        resp = resp['cpc:classification-item']
    try:
        return resp['cpc:class-title']['cpc:title-part'][0]['cpc:text']['$']
    except:
        return resp['cpc:class-title']['cpc:title-part']['cpc:text']['$']

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get('https://worldwide.espacenet.com/3.2/rest-services/classification/cpc/H04L29/08.json?depth=0&interleave&ancestors&navigation&origin=https_worldwide_espacenet_com', headers=headers)

def get_epo_records(pa, page_no):
    import requests

    cookies = {
        'cpcops_settings': '%7B%22display_tree%22%3Atrue%2C%22show-2000-series%22%3A%22state-1%22%2C%22dateRange%22%3A%7B%22from%22%3A%7B%22month%22%3A10%2C%22year%22%3A2020%7D%2C%22to%22%3A%7B%22month%22%3A10%2C%22year%22%3A2020%7D%2C%22isRange%22%3Afalse%7D%7D',
        'cart': '%5B%5D',
        'menuCurrentSearch': '%2F%2Fworldwide.espacenet.com%2FsearchResults%3FAB%3D%26AP%3D%26CPC%3D%26DB%3DEPODOC%26IC%3D%26IN%3D%26PA%3DIBM%26PD%3D%26PN%3D%26PR%3D%26ST%3Dadvanced%26Submit%3DSearch%26TI%3D%26locale%3Den_EP',
        'PGS': '10',
        'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE': 'en_EP',
        'currentUrl': 'https%3A%2F%2Fworldwide.espacenet.com%2FadvancedSearch%3Flocale%3Den_EP',
        'LevelXLastSelectedDataSource': 'EPODOC',
        'JSESSIONID': 'pj65Yu3t6ExqToR9SkYMX03O.espacenet_levelx_prod_1',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
        'Accept': 'application/json,application/i18n+xml',
        'X-EPO-PQL-Profile': 'cpci',
        'EPO-Trace-Id': 'ylzamx-9sx0g6-AAA-000176',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://worldwide.espacenet.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://worldwide.espacenet.com/patent/search?q=pa%3D%22IBM%22',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    params = (
        ('lang', 'en,de,fr'),
        ('q', 'pa="'+pa+'"'),
        ('qlang', 'cql'),
        ('p_s', 'espacenet'),
        ('p_q', 'pa="'+pa+'"'),
    )

    data = '{"query":{"fields":["publications.ti_*","publications.abs_*","publications.pn_docdb","publications.in","publications.in_country","publications.pa","publications.pa_country","publications.pd","publications.pr_docdb","publications.app_fdate.untouched","publications.ipc","publications.ipc_ic","publications.ipc_icci","publications.ipc_iccn","publications.ipc_icai","publications.ipc_ican","publications.ci_cpci","publications.ca_cpci","publications.cl_cpci","biblio:pa;pa_orig;pa_unstd;in;in_orig;in_unstd;pa_country;in_country;pd;pn;allKindCodes;","oprid_full.untouched","opubd_full.untouched"],"from":' + str(page_no*20) + ',"size":20,"highlighting":[{"field":"publications.ti_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_en","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.ti_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_de","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.ti_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.abs_fr","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pn","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pn_docdb","fragment_words_number":20,"number_of_fragments":3,"hits_only":true},{"field":"publications.pa","fragment_words_number":20,"number_of_fragments":3,"hits_only":true}],"sort":{"field":"oprid_full","order":"desc"}},"filters":{"publications.patent":[{"value":["true"]}]},"widgets":{}}'

    response = requests.post('https://worldwide.espacenet.com/3.2/rest-services/search', headers=headers, params=params, cookies=cookies, data=data)
    return response.json()


