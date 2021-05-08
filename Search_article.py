import warnings
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.common.exceptions import NoSuchElementException 
import re


chromedriver_path = r'/home/hamza/Desktop/Selenium_project/chromedriver_linux64/chromedriver'

def check_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output
    except NoSuchElementException:
        return " "

warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(driver, 10)

driver.get('https://www.google.com/search?q=%22bp%22+site%3Ahttps%3A%2F%2Fwww.bloomberg.com%2F&safe=active&client=firefox-b-1-d&biw=1430&bih=644&tbs=sbd%3A1%2Cqdr%3Aw&tbm=nws&ei=BjOUYPuYIJbr-gShk7fgDw&oq=%22bp%22+site%3Ahttps%3A%2F%2Fwww.bloomberg.com%2F&gs_l=psy-ab.3...2966.3055.0.3455.2.2.0.0.0.0.102.179.1j1.2.0....0...1c.1.64.psy-ab..0.0.0....0.aliliFf8mUY')

soup = BeautifulSoup(driver.page_source, 'html.parser')
posts_article = soup.findAll('div', {'class': 'dbsr'})
article_url = []
for x in range(len(posts_article)):
    time_line = driver.find_element_by_css_selector('div[id="rso"]>div:nth-child('+ str(x+1) +') div[class="dbsr"]>a span[class="WG9SHc"]')
    
    if(time_line.text == "1 day ago" or re.findall('(.* hou(.*) ago)', time_line.text) or  re.findall('(.* min(.*) ago)', time_line.text)):
        link = soup.select_one('div[id="rso"]>div:nth-child('+ str(x+1) +') div[class="dbsr"]>a[href]')
        article_url.append(link['href'])

print(article_url) 
driver.close()

date = []
name = []
author = []
source = []
url_article = []
for url in article_url:
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    print(url)
    driver.get(url)
    time.sleep(15)
    button = check_exists_by_css(driver,'div[class*="innerModal"] button[title="Close"]')
    if button != " ":
        button.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = driver.find_element_by_tag_name('body')
    bp_search = re.findall('(BP)', data.text)
    print(data.text)
    print(bp_search)
    print(len(bp_search))
    if len(bp_search) >= 3:
        url_article.append(url)
        date.append(driver.find_element_by_css_selector('time[class="article-timestamp"]').text)
        name_check = check_exists_by_css(driver,'h1[class="lede-text-v2__hed"]')
        if(name_check != " "):
            name.append(name_check.text)
        else:
            name_check = check_exists_by_css(driver,'div[class="lede-newsletter__newsletter-headline"]')
            name.append(name_check.text)
        author.append(driver.find_element_by_css_selector('div[class="author-v2"]>a').text)
        source.append('bloomberg')
    time.sleep(30)
    driver.close()
complete_data = {}
complete_data['Date'] = date
complete_data['Article_url'] = url_article
complete_data['Article_name'] = name
complete_data['Author'] = author
complete_data['Source'] = source


Data = pd.DataFrame(complete_data)
Data.to_excel('Output.xlsx' ,index=None)
print("Complete Now Thanks You")



      