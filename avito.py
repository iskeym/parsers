import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def categories(driver, categories):
    avito = 'https://www.avito.ru'
    driver.get(avito)

    button = driver.find_element(By.XPATH, "//span[@class='top-rubricator-more-G5sAi text-text-LurtD text-size-s-BxGpL']").click()
    time.sleep(1)

    items = driver.find_elements(By.TAG_NAME, 'li')
    for item in items:
        try:
            categories_link = item.find_element(By.CLASS_NAME, "link-design-default-_nSbv").get_attribute('href')
            categories.append(categories_link)

            print(categories_link)
        except Exception:
            pass

def informations(driver, categories, x):
    for category in categories:
        driver.get(category)

        pages = driver.find_element(By.XPATH, "//div[@class='pagination-root-Ntd_O']//span[8]").text

        for page in range(1, int(pages) + 1):
            url = (f'{category}&p={page}')
            driver.get(url)

            items = driver.find_elements(By.CLASS_NAME, "iva-item-titleStep-pdebR")

            for item in items:
                x.append({
                    'title': item.find_element(By.CLASS_NAME, "title-root-zZCwT").text,
                    'link': item.find_element(By.CLASS_NAME, "link-link-MbQDP").get_attribute('href')
                })

                print(x)

def save(total):
    with open('avito.csv', 'w', newline='') as ex:
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
    os.startfile('avito.csv')

    driver.close()

parser()