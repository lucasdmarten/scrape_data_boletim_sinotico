from urllib import response
from selenium import webdriver
from pandas import date_range, to_datetime, DataFrame
import helpers
from bs4 import BeautifulSoup
import os
import time

CFG = helpers.load_cfg()
FMT = '%Y%m%d%H'

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
    return [to_datetime(d) for d in date_range(start, end, freq='6H')]


if __name__ == "__main__":
        
    for date_obj in gen_list_dates('20090101T00', '20090103T00'):

        if date_obj.strftime('%H') in ["00", "12", "18"]:
            date_rod = date_obj.strftime(FMT)
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

                    os.system(f"mkdir -p ./data/{date_obj.strftime('%Y')}/{level}")
                    
                    resp = dict()
                    resp["dates"] = [date_rod]
                    resp["text_data"] = [text]
                    resp["url_data"] = [url]
                    resp["prev24"] = [soup.find_all('a')[-1].get_attribute_list('href')[0].split("'")[1]]
                    resp["prev48"] = [soup.find_all('a')[-2].get_attribute_list('href')[0].split("'")[1]]
                    resp["prev72"] = [soup.find_all('a')[-3].get_attribute_list('href')[0].split("'")[1]]
                    resp["prev96"] = [soup.find_all('a')[-4].get_attribute_list('href')[0].split("'")[1]]
                    resp["prev120"] = [soup.find_all('a')[-5].get_attribute_list('href')[0].split("'")[1]]
                    print(resp)
            
                    DataFrame(resp).to_csv(f'./data/{date_obj.strftime("%Y")}/{level}/{level}_{date_rod}.csv')
            time.sleep(3)
            helpers.switch_to_tab_by_index(driver, driver.window_handles[0])
