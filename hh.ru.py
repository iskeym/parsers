import math
import os
import csv
import time
from pyppeteer_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def categories(driver, categories):
    driver.get('https://hh.ru/catalog?hhtmFrom=main')

    items = driver.find_elements(By.CLASS_NAME, "catalog__item")
    for item in items:
        category = item.find_element(By.CLASS_NAME, "catalog__item-link").get_attribute('href')
        print(category)

        categories.append(category)

        print(categories)

def informations(driver, categories, x):
    for category in categories:
        driver.get(category)

        quantity = driver.find_element(By.XPATH, "//span[@class='bloko-header-section-3']").text.replace(', ', '').replace(' вакансий', '').replace(' вакансии', '').replace(' вакансия', '')
        pages = float(quantity) / 50

        for page in range(1, math.ceil(pages)):
            driver.get(f'{category}?page={page}')

            items = driver.find_elements(By.CLASS_NAME, "vacancy-serp-item")

            for item in items:
                x.append({
                    'title': item.find_element(By.CLASS_NAME, "bloko-link").text,
                    'link': item.find_element(By.CLASS_NAME, "bloko-link").get_attribute('href')
                })

                print(x)
                total.extend(x)

def save(total):
    with open('hh.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['Название', 'Ссылка'])
        for dict in total:
            writer.writerow([dict['title'], dict['link']])

def parser():
    driver = webdriver.Chrome()
    stealth(driver,
        languages=["en-US", "en"],
        vendor='Google Inc.',
        platform='Win64',
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )

    categories_link = []
    categories(driver, categories_link)

    x = []
    informations(driver, categories_link, x)

    save(x)
    os.startfile('hh.csv')

    driver.close()

parser()