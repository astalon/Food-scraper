from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import os
import time

import scraper

loaded = 0

def load_more(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #element = driver.find_element_by_class_name("showMoreText")
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "showMoreText")))
        element.click()
    except:
        print("Something went wrong loading more recipes")
    
    return driver


# //*[@id="recipes"]/article[2]/div[2]/header/h2/a
def get_org_article_xpath(number):
    return "//*[@id='recipes']/article[" + str(number+2) + "]/div[2]/header/h2/a"

def get_loaded_article_xpath(number, loaded):
    return "//*[@id='recipes']/div[" + str(loaded+1) + "]/article[" + str(number+2) + "]/div[2]/header/h2/a"


def fetch_loaded_recipes(driver, loaded):

    for i in range(16):

        xpath = get_loaded_article_xpath(i, loaded)

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            scraper.scrape(element.get_attribute('href'))
        except:
            print("Something went wrong while finding element or scraping for newly loaded for index " + str(i+2) + " and load " + str(loaded))


wd = os.getcwd()
ingredients_json = {}
instructions_json = {}

opts = webdriver.FirefoxOptions()
opts.headless = False

firefox_binary = FirefoxBinary('/usr/bin/firefox')
driver = webdriver.Firefox(firefox_binary=firefox_binary, options=opts)

start_url = "https://www.ica.se/recept/smaratter/"
driver.get(start_url)

for i in range(16):
    xpath = get_org_article_xpath(i)
    
    try:
        #element = driver.find_element_by_xpath(xpath)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        scraper.scrape(element.get_attribute('href'))
    except:
        print("Something went wrong while finding element or scraping for index " + str(i+2))

loads = 5
for i in range(loads):
    driver = load_more(driver)
    loaded += 1
    fetch_loaded_recipes(driver, loaded)


driver.quit()