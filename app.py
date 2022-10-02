from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pandas import date_range, to_datetime, DataFrame
import helpers
import requests
from bs4 import BeautifulSoup
import time, os

CFG = helpers.load_cfg()

driver = webdriver.Firefox()
driver.get(CFG["url"])

def get_new_tab(driver, date_obj):
    helpers.select_element(driver, CFG['id_elements']['hour'], date_obj.strftime('%H'))
    helpers.select_element(driver, CFG['id_elements']['day'], date_obj.strftime('%d'))
    helpers.select_element(driver, CFG['id_elements']['month'], date_obj.strftime('%m'))
    helpers.select_element(driver, CFG['id_elements']['year'], date_obj.strftime('%Y'))
    helpers.click_button(driver)
    return 

def gen_list_dates(start, end):
    return [to_datetime(d) for d in date_range(start, end, freq='12H')]


for date_obj in gen_list_dates('20080901T00', '20081231T12'):
    fmt = '%Y%m%d%H'
    date_rod = date_obj.strftime(fmt)
    print(date_rod)
    home_tab = helpers.get_current_tab(driver=driver)
    get_new_tab(driver, date_obj)

    if home_tab == helpers.get_current_tab(driver=driver):
        helpers.switch_to_tab_by_index(driver, driver.window_handles[-1])

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.find_all(class_="texto")
        
        dates = list()
        text_data = list()
        url_data = list()
        level_data = list()
        prev24 = list()
        prev48 = list()
        prev72 = list()
        prev96 = list()
        prev120 = list()
        for i, data in enumerate(texts):
            
            if data.find('a'):
                level = CFG['structure_chart'][i]
                url = data.find('a').get_attribute_list('href')[0].split("'")[1]
                text = data.text
                dates.append(date_rod)
                text_data.append(text)
                url_data.append(url)
                level_data.append(level)
                prev24.append(soup.find_all('a')[-1].get_attribute_list('href')[0].split("'")[1])
                prev48.append(soup.find_all('a')[-2].get_attribute_list('href')[0].split("'")[1])
                prev72.append(soup.find_all('a')[-3].get_attribute_list('href')[0].split("'")[1])
                prev96.append(soup.find_all('a')[-4].get_attribute_list('href')[0].split("'")[1])
                prev120.append(soup.find_all('a')[-5].get_attribute_list('href')[0].split("'")[1])

        os.system(f"mkdir -p ./data/{date_obj.strftime('%Y')}/")
        
        response = {
            "dates":dates,
            "text_data":text_data,
            "url_data":url_data,
            "level_data":level_data,
            "prev24":prev24,
            "prev48":prev48,
            "prev72":prev72,
            "prev96":prev96,
            "prev120":prev120
        }
        DataFrame(response).to_csv(f'./data/{date_obj.strftime("%Y")}/{date_rod}.csv')

    helpers.switch_to_tab_by_index(driver, driver.window_handles[0])

