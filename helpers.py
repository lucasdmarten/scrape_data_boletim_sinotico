from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import yaml

def load_cfg():
    with open('config.yml') as yfile:
        return yaml.safe_load(yfile)

def get_driver():    
    driver = webdriver.Firefox()
    driver.get("https://tempo.cptec.inpe.br/boletim-tecnico/faces/buscar.jsp")
    return driver

def select_element(driver, id, i):
    select = Select(driver.find_element(By.ID, id))
    select.select_by_value(i)
    return 

def click_button(driver):
    driver.find_element(By.CLASS_NAME, 'botao').click()

def get_current_tab(driver):
    current_tab = driver.current_window_handle
    return current_tab

def get_tabs(driver):
    tabs = driver.window_handles

def switch_to_tab_by_index(driver, tab):
    driver.switch_to.window(tab)
    return 
