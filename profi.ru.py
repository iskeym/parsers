import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def categories(driver, categories):
    driver.get('https://profi.ru/services/repetitor/')

    items = driver.find_elements(By.CLASS_NAME, "services-catalog__item")
    for item in items:
        categories_link = item.get_attribute('href')
        categories.append(categories_link)

        print(categories_link)

    categories.pop(-1)

def open(driver):
    driver.get('https://irkutsk.profi.ru/repetitor/dvi/dvi-tvorcheskii-konkurs/dvi-tvorcheskii-konkurs-(akterskoe-masterstvo)/')

    button = driver.find_element(By.XPATH, "//a[@class='ui_2QW3c ui_2Abw3 ui__HiyL _gfp1g0A']//span[@class='ui_3vUWP']").click()
    time.sleep(3)

    button2 = driver.find_element(By.XPATH, "//body//li[3]").click()
    time.sleep(2)

def scroll(driver):
    while True:
        try:
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.END)

            button = driver.find_element(By.XPATH, "//button[@class='ui_2QW3c ui_2Abw3 ui_3aY4S pagination__show-more']").click()

            time.sleep(2)
        except:
            break

def informations(driver, categories, x):
    for category in categories:
        driver.get(category)

        open(driver)
        scroll(driver)

        items = driver.find_elements(By.XPATH, "//a[@class='ui_1hi7c ui_RF7aD ui_3j-OD']")

        for item in items:
            x.append({
                'title': item.text,
                'link': item.get_attribute('href')
            })

            print(x)

def save(total):
    with open('profi.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['Название', 'Ссылка'])
        for dict in total:
            writer.writerow([dict['title'], dict['link']])

def parser():
    driver = webdriver.Chrome()

    categories_link = []
    categories(driver, categories_link)

    x = []
    informations(driver, categories_link, x)

    save(x)
    os.startfile('profi.csv')

    driver.close()

parser()