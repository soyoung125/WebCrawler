# Step 1. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time, sys, math, os

print("=" * 80)
print(" 아산병원 질병데이터 - 저장할 내용을 목록으로 만들어서 xls , csv 형식으로 저장하기")
print("=" * 80)

# query_txt = input('1.크롤링할 키워드는 무엇입니까?: ')
# cnt = int(input('2.수집할 데이터는 몇 건입니까?: '))
# page_cnt = math.ceil(cnt / 30)  # 페이지 수 구함(스크롤수)
cnt = 20

f_dir = input('3.결과를 저장할 폴더이름을 입력해주세요(기본경로: c:\\py_temp\\) :')
if f_dir == '':
    f_dir = 'c:\\py_temp\\'

# Step 2. 크롬 드라이버를 설정하고 검색을 수행하여 View 메뉴 클릭
driver = webdriver.Chrome("c:/py_temp/chromedriver.exe")

driver.get('https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseSubmain.do')
time.sleep(2)

# driver.maximize_window()
# time.sleep(2)

driver.find_element_by_class_name("menu3").click()
# driver.find_element_by_class_name("listCon")
# element = driver.find_elements_by_class_name("listCon")
# element[0].click()
driver.find_element_by_link_text('감염성질환').click()
# for i in element:
#     i.click()


# Step 3.각 데이터 저장용 리스트 생성 후 자동 스크롤 다운 수행

no2 = []  # 질병 번호 컬럼
name2 = []  # 질병명 컬럼
symptom2 = []  # 질병 증상 컬럼
diseases2 = []  # 관련질병 컬럼
department2 = []  # 진료과 컬럼

# 자동 스크롤다운 함수
# def scroll_down(driver):
#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
#     time.sleep(3)


# if page_cnt > 2:
#     i = 1
#     while (i <= page_cnt):
#         scroll_down(driver)
#         i += 1
#         print('%s 페이지 정보를 추출하고 있으니 잠시만 기다려 주세요~~^^' % i)
#
# print("\n")

# Step 4. 주요 내용을 추출하여 리스트에 저장
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
pages = soup.find('div', 'pagingWrapSec').find_all('a')

disease_no = 1  # 질병 번호용 변수


# 해당 페이지의 데이터 수집
def disease_scraping():
    global disease_no
    view_list = soup.find('ul', 'descBox').find_all('li')

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

            # 질병 명 리스트에 추가
            name2.append(title[0].get_text())
            print('2.질병명:', title[0].get_text())

            # 질병 증상
            if(all_title[0].get_text() == '증상'):
                symptom = all_cont[0].get_text()
                symptom2.append(symptom)
                print('3.증상:', symptom)
            else:
                symptom2.append("")

            # 관련질병
            if (all_title[1].get_text() == '관련질환'):
                diseases = all_cont[1].get_text()
                diseases2.append(diseases)
                print('4.관련질병:', diseases)
            else:
                diseases2.append('')

            # 진료과
            # depm = all_title[2].get_text()
            if len(all_title) > 2 and all_title[2].get_text() == '진료과':
                department = all_cont[2].get_text()
                department2.append(department)
                print('5.진료과:', department)
            else:
                department2.append('')

            print("\n")

            disease_no += 1


# 페이지 이동
for i in pages:
    driver.find_element_by_link_text(i.get_text()).click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    disease_scraping()


# Step 5.출력 결과를 표(데이터 프레임) 형태로 만들기


import openpyxl

asan_diseases = pd.DataFrame()
asan_diseases['번호'] = no2
asan_diseases['질병명'] = pd.Series(name2)
asan_diseases['증상'] = pd.Series(symptom2)
asan_diseases['관련질환'] = pd.Series(diseases2)
asan_diseases['진료과'] = pd.Series(department2)

# Step 6. 저장될 파일위치와 이름을 지정한 후 csv , xls 파일로 저장하기
n = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)

sec_name = 'asan_diseases'
# os.makedirs(f_dir + s + '-' + element[0].get_text() + '-' + sec_name)
# os.chdir(f_dir + s + '-' + element[0].get_text() + '-' + sec_name)
os.makedirs(f_dir + s + '-감염성질환-' + sec_name)
os.chdir(f_dir + s + '-감염성질환-' + sec_name)

# fc_name = f_dir + s + '-' + element[0].get_text() + '-' + sec_name + '\\' + s + '-' + element[0].get_text() + '-' + sec_name + '.csv'
# fx_name = f_dir + s + '-' + element[0].get_text() + '-' + sec_name + '\\' + s + '-' + element[0].get_text() + '-' + sec_name + '.xlsx'
fc_name = f_dir + s + '-감염성질환-' + sec_name + '\\' + s + '-감염성질환-' + sec_name + '.csv'
fx_name = f_dir + s + '-감염성질환-' + sec_name + '\\' + s + '-감염성질환-' + sec_name + '.xlsx'


# csv 형태로 저장하기
asan_diseases.to_csv(fc_name, encoding="utf-8-sig", index=False)
print(" csv 파일 저장 경로: %s" % fc_name)

# 엑셀 형태로 저장하기
asan_diseases.to_excel(fx_name, index=False, engine='openpyxl')
print(" xls 파일 저장 경로: %s" % fx_name)

driver.close()