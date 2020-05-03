from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from wcl_api.models import Parse
import time

def get_parses(report, fights):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(executable_path='C:\\chromedriver.exe', options=options)
    parses = []

    for fight in fights.kills:
        types = ['healing', 'damage-done']

        for parse_type in types:
            url = build_url(report, fight, parse_type)
            print('retrieving url: ' + url)
            driver.get(url)
            time.sleep(3)

            table = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('main-table-0'))
            rows = table.find_elements(By.CSS_SELECTOR, 'tbody > .odd, tbody > .even')

            for row in rows:
                parse = Parse(fight, row, parse_type)
                parses.append(parse)

    driver.close()
    
    return parses

def build_url(report, fight, parse_type):
    web_link_base = 'https://www.warcraftlogs.com/reports/{0}#fight={1}&type={2}'
    
    return web_link_base.format(report.id_string, fight['id'], parse_type)