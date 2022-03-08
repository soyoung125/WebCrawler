# 질병관리청에서 사용할 질병 데이터를 건강정보 신청 리스트에 추가

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time, sys, math, os

print("=" * 80)
print("질병관리청 사용할 질병 데이터 리스트에 추가")
print("=" * 80)


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# driver = webdriver.Chrome("c:/py_temp/chromedriver.exe")
driver = set_chrome_driver()

driver.get('https://health.kdca.go.kr/healthinfo/biz/health/main/mainPage/main.do')
time.sleep(2)

driver.find_element(By.CLASS_NAME, "btn-login").click()
# driver.find_element_by_id("userId_input").click()
# driver.find_element_by_id("userId_input").send_keys('fkqhd1025' + '\n') #아이디 쓰기
# driver.find_element(By.ID, "userId_input").send_keys('fkqhd1025' + '\n')
#
time.sleep(30)

driver.find_element(By.CLASS_NAME, "visual-box03").click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
pages = soup.find('div', class_='pagination').find_all('a')
disease_list = []

driver.find_element(By.XPATH, '//*[@id="healthLayoutForm"]/div[1]/div/a[3]').click()
driver.find_element(By.LINK_TEXT, "고객문의").click()


# def add_disease():
#     for i in disease_list:
#         print(i.get_text().strip())
#         driver.find_element(By.LINK_TEXT, i.get_text().strip()).click()
#         time.sleep(1)
#         driver.find_element(By.CLASS_NAME, 'btn-white').click()
#         try:
#             alert = driver.switch_to_alert()
#             # alert = Alert(driver)
#             alert.accept()
#         except:
#             print('no alert')
#         time.sleep(1)
#         driver.back()
#         driver.back()
#
#
# driver.find_element(By.LINK_TEXT, "질병 및 장애").click()
# for p in range(1,7):
#     driver.find_element(By.LINK_TEXT, str(p))
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     disease_list = soup.find('div', class_='hd-indexbox').find('ul').find_all('a')
#     add_disease()
