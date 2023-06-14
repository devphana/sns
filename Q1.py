import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib3.exceptions import InsecureRequestWarning
import csv
import time
import requests
import os
import urllib3

keyword = input("검색어를 입력하세요: ")
from_date = input("조회 시작 날짜를 입력하세요 (YYYY/MM/DD): ")
to_date = input("조회 종료 날짜를 입력하세요 (YYYY/MM/DD): ")
file_path = input("파일 저장 경로를 입력하세요: ")
count = int(input("몇 페이지까지 필요하신가요(1이상정수):"))

# 웹 드라이버 실행
driver = webdriver.Chrome("C:/Users/rl/Desktop/py/chromedriver_win32/chromedriver.exe")
driver.get("https://www.g2b.go.kr/index.jsp")

# 검색어 입력
search_input = driver.find_element(By.ID, "bidNm")
search_input.send_keys(keyword)

# 조회 시작 날짜 입력

from_date_input = driver.find_element(By.ID, "fromBidDt")
from_date_input.clear()
from_date_input.send_keys(from_date)

# 조회 종료 날짜 입력

to_date_input = driver.find_element(By.ID, "toBidDt")
to_date_input.clear()
to_date_input.send_keys(to_date)

time.sleep(2)

# 검색 버튼 클릭
search_button = driver.find_element(By.CLASS_NAME, "btn_dark")
search_button.click()

time.sleep(2)

driver.switch_to.frame('sub')
driver.switch_to.frame('main')

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

    # 헤더 추출
headers = []
header_cells = soup.select('div > table > thead > tr > th')
for cell in header_cells:
        headers.append(cell.text.strip())

    # 데이터 추출
data = []
rows = soup.select('div > table > tbody > tr')
for row in rows:
    cells = row.select('td')
    row_data = [cell.text.strip() for cell in cells]
    data.append(row_data)

if count ==1:
    # DataFrame 생성
    df = pd.DataFrame(data, columns=headers)

    # 추출한 데이터 확인
    csv_file_path = os.path.join(file_path , 'output.csv')
    df.to_csv(csv_file_path, index=False,encoding='utf-8-sig')
    print("CSV 파일이 저장되었습니다:", csv_file_path)

    # Excel 파일로 저장
    excel_file_path =os.path.join(file_path , 'output.xlsx')
    df.to_excel(excel_file_path, index=False,encoding='utf-8')
    print("Excel 파일이 저장되었습니다:", excel_file_path)
    # 웹 드라이버 종료
    driver.quit()
else:
    for i in range(count-1):

        wait = WebDriverWait(driver, 40)

        # "더보기" 링크 대기 및 클릭
        more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='default' and contains(@href, 'to_more(1)')]")))
        more_button.click()

        time.sleep(2)

        rows = soup.select('div > table > tbody > tr')
        for row in rows:
            cells = row.select('td')
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)

    
    df = pd.DataFrame(data, columns=headers)

    # 추출한 데이터 확인
    csv_file_path = os.path.join(file_path , 'output.csv')
    df.to_csv(csv_file_path, index=False,encoding='utf-8-sig')
    print("CSV 파일이 저장되었습니다:", csv_file_path)

    # Excel 파일로 저장
    excel_file_path =os.path.join(file_path , 'output.xlsx')
    df.to_excel(excel_file_path, index=False,encoding='utf-8')
    print("Excel 파일이 저장되었습니다:", excel_file_path)

    # 웹 드라이버 종료
    driver.quit()                










