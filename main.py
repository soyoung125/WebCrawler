# Step 1. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time, sys, math, os

print("=" * 80)
print(" 아산병원 질병데이터 - 저장할 내용을 목록으로 만들어서 xls , csv 형식으로 저장하기")
print("=" * 80)

f_dir = 'c:\\py_temp\\'


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# Step 2. 크롬 드라이버를 설정하고 검색을 수행하여 View 메뉴 클릭
driver = set_chrome_driver()

driver.get('https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseSubmain.do')
time.sleep(2)

driver.find_element_by_class_name("menu3").click()

no2 = []  # 질병 번호 컬럼
disease_type2 = []  # 질병 대분류 컬럼
name2 = []  # 질병명 컬럼
symptom2 = []  # 질병 증상 컬럼
diseases2 = []  # 관련질병 컬럼
department2 = []  # 진료과 컬럼
synonym2 = []  #동의어

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
pages = []
tab_list = soup.find('div', class_='tabSearchList cont2').find('ul', class_='tabSearchListUl clearfix').find_all('a')

disease_no = 1  # 질병 번호용 변수
disease_type = '' # 질환 대분류


# 해당 페이지의 데이터 수집
def disease_scraping(soup1):
    global disease_no
    view_list = soup1.find('ul', 'descBox').find_all('li')

    for i in view_list:
        try:
            title = i.find('div', class_='contBox').find_all('strong')
            all_title = i.find('dl').find_all('dt')
            all_cont = i.find('dl').find_all('dd')
        except:
            continue
        else:
            # 질병 번호 리스트에 추가
            no2.append(disease_no)
            print('1.번호:', disease_no)

            # 질병 대분류 리스트에 추가
            disease_type2.append((disease_type))
            print('2.대분류:', disease_type)

            # 질병 명 리스트에 추가
            title = title[0].get_text()
            name2.append(' '.join(title.split()))
            print('3.질병명:', ' '.join(title.split()))

            # 질병 증상
            if (all_title[0].get_text() == '증상'):
                symptom = all_cont[0].get_text()
                symptom2.append(' '.join(symptom.split()))
                print('4.증상:', ' '.join(symptom.split()))
            else:
                symptom2.append("")

            # 관련질병
            if (all_title[1].get_text() == '관련질환'):
                diseases = all_cont[1].get_text()
                diseases2.append(' '.join(diseases.split()))
                print('4.관련질병:', ' '.join(diseases.split()))
            else:
                diseases2.append('')

            # 진료과
            if len(all_title) > 2 and all_title[2].get_text() == '진료과':
                department = all_cont[2].get_text()
                department2.append(' '.join(department.split()))
                print('5.진료과:', ' '.join(department.split()))
            else:
                department2.append('')

            # 진료과
            if len(all_title) > 3 and all_title[3].get_text() == '동의어':
                synonym = all_cont[3].get_text()
                synonym2.append(' '.join(synonym.split()))
                print('5.동의어:', ' '.join(synonym.split()))
            else:
                synonym2.append('')

            print("\n")

            disease_no += 1


# 페이지 이동
def move_pages():
    for p in pages:
        driver.find_element_by_link_text(p.get_text()).click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        disease_scraping(soup)


for i in tab_list:
    disease_type = i.get_text()
    driver.find_element_by_link_text(disease_type).click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', 'pagingWrapSec').find_all('a')
    move_pages()

# Step 5.출력 결과를 표(데이터 프레임) 형태로 만들기


import openpyxl

asan_diseases = pd.DataFrame()
asan_diseases['번호'] = no2
asan_diseases['대분류'] = pd.Series(disease_type2)
asan_diseases['질병명'] = pd.Series(name2)
asan_diseases['증상'] = pd.Series(symptom2)
asan_diseases['관련질환'] = pd.Series(diseases2)
asan_diseases['진료과'] = pd.Series(department2)
asan_diseases['동의어'] = pd.Series(synonym2)

# Step 6. 저장될 파일위치와 이름을 지정한 후 csv , xls 파일로 저장하기
n = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)

sec_name = 'asan_diseases'
os.makedirs(f_dir + s + '-아산병원질병데이터-' + sec_name)
os.chdir(f_dir + s + '-아산병원질병데이터-' + sec_name)

fc_name = f_dir + s + '-아산병원질병데이터-' + sec_name + '\\' + s + '-아산병원질병데이터-' + sec_name + '.csv'
fx_name = f_dir + s + '-아산병원질병데이터-' + sec_name + '\\' + s + '-아산병원질병데이터-' + sec_name + '.xlsx'

# csv 형태로 저장하기
asan_diseases.to_csv(fc_name, encoding="utf-8-sig", index=False)
print(" csv 파일 저장 경로: %s" % fc_name)

# 엑셀 형태로 저장하기
asan_diseases.to_excel(fx_name, index=False, engine='openpyxl')
print(" xls 파일 저장 경로: %s" % fx_name)

driver.close()
