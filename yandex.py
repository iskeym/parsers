import os
import csv
import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def all_categories(driver, categories_all):
    driver.get('https://uslugi.yandex.ru/?utm_campaign=ssa_brand_ru.ru_alldevices_hand.roi&utm_content=gid%7C4794988767%7Caid%7C11621963348%7C35916239979&utm_medium=search&utm_source=yandex&utm_term=яндекс%20услуги&yclid=1167185313908447839')

    time.sleep(2)
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)

    time.sleep(2)

    button = driver.find_element(By.XPATH, "//a[11]//span[1]").click()

    time.sleep(3)

    items = driver.find_elements(By.XPATH, "//div[@class='HomeRubricMenu-MenuItem']//a[@class='Link']")
    for item in items:
        category = item.get_attribute('href')
        print(category)

        categories_all.append(category)

def category(driver, categories_all, categories_link):
    x = []

    items = driver.find_elements(By.CLASS_NAME, "HomeRubricMenu-ContentItem")
    for item in items:
        category = item.find_element(By.CLASS_NAME, "Link").get_attribute('href')
        print(category)

        categories_link.append(category)

    for categories in categories_all:
        driver.get(categories)

        items = driver.find_elements(By.CLASS_NAME, "HomeRubricMenu-ContentItem")
        for item in items:
            category = item.find_element(By.CLASS_NAME, "Link").get_attribute('href')
            print(category)

            categories_link.append(category)

def informations(driver, categories_link, x):
    for category in categories_link:
        driver.get('https://uslugi.yandex.ru/976-bratsk/category/kompyuteryi-i-it/razrabotka-na-python--4789?p=3&utm_campaign=ssa_brand_ru.ru_alldevices_hand.roi&utm_content=gid%7C4794988767%7Caid%7C11621963348%7C35916239979&utm_medium=search&utm_source=yandex&utm_term=яндекс%20услуги&yclid=1167185313908447839')

        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 700)")
        time.sleep(2)

        quantity = driver.find_element(By.XPATH, "//b[@class='Text Text_line_m Text_size_m Text_type_bold TextBlock']").text.replace(' специалистов', '')
        pages = float(quantity) / 10

        for page in range(0, math.ceil(pages)):
            url = (f'{category}&p={page}')
            driver.get(url)

            items = driver.find_elements(By.XPATH, "//a[@class='Link WorkerCard-Title']")
            for item in items:
                try:
                    x.append({
                        'title': item.text,
                        'link': item.get_attribute('href')
                    })
                    print(x)
                except:
                    pass
        print(x)

def save(total):
    with open('profi.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['Название', 'Ссылка'])
        for dict in total:
            writer.writerow([dict['title'], dict['link']])

def parser():
    driver = webdriver.Chrome()

    categories_all = []
    all_categories(driver, categories_all)
    categories_link = []
    category(driver, categories_all, categories_link)

    x = []
    informations(driver, categories_link, x)

    driver.close()

parser()