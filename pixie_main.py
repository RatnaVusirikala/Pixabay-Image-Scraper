import re
import os
import time
import ssl
import requests
import lxml
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pathlib import Path
import selenium
from selenium import webdriver
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from lxml import etree


def scroll_down(driver):
    page_height = driver.execute_script("return document.body.scrollHeight")
    total_scrolled = 0
    for i in range(page_height):
        driver.execute_script(f'window.scrollBy(0,{i});')
        total_scrolled += i
        if total_scrolled >= page_height/2:
            last_no = i
            break

    for i in range(last_no, 0, -1):
        driver.execute_script(f'window.scrollBy(0,{i});')


def imagescrape(item):
    try:
        # Script params
        # service = webdriver.ChromeService()
        output_dir = './Pixabay'  # path to output
        # url to the images
        base_url = f'https://pixabay.com/images/search/{item}/'
        # page_max = 10  # Max nb of page to scroll
        # page_start = 1  # In case you want to resume
        # Create output directory if needed
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # Script start
        options = Options()
        # options.add_argument("--headless=new")
        driver = webdriver.Chrome(
            executable_path=r'C:\Users\Pandu\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe', options=options)

        links = []
        alts = []
        flag = False
        i=1
        while True:
            url = base_url + '?pagi=' + str(i)
            driver.get(url)
            i+=1
            scroll_down(driver)
            data = driver.execute_script(
                'return document.documentElement.outerHTML')
            scraper = BeautifulSoup(data, 'lxml')

            if scraper.find_all(string=re.compile('^Try another search term$')):
                print("\nNo Results 1")
                driver.close()
                return

            articles_count = scraper.findAll('a', attrs={'class': 'link--WHWzm'})

            if (articles_count):
                for unit in articles_count:
                    if articles_count.index(unit) == 0:
                        temp = unit.find('img')['src']
                        if temp in links:
                            flag = True
                            break
                    links.append(unit.find('img')['src'])
                    alts.append(unit.find('img')['alt'])

            else:
                print("\nNo Images")
                break
            if flag:
                break

        data_dic = {}
        data = pd.DataFrame(data_dic)
        data['Links'] = links
        data['title'] = alts

        data = data.drop_duplicates()
        item = item.replace(' ', '-')
        data.to_csv(output_dir + '/' + item + '.csv')
        driver.close()
    except Exception as e:
        print(e)


def main() -> None:
    text_file = open("search_words.txt", "r")
    lines = text_file.readlines()
    text_file.close()
    print('\n--------------- scrapping started ---------------')
    for item in tqdm(lines, desc='SCRAPING'):
        item = item.strip()
        print('\n--------------- ' + item + ' started ---------------')
        imagescrape(item)
        print('\n--------------- ' + item + ' completed ---------------')
    print('\n--------------- scrapping completed ---------------')


if __name__ == '__main__':
    main()
