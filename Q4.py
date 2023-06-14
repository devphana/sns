from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
from urllib3.exceptions import InsecureRequestWarning



# 사용자 입력 받기
keyword = input("검색 키워드를 입력하세요:")
quantity = int(input("수집할 PDF 파일의 수량을 입력하세요:"))
save_path = input("저장할 경로를 입력하세요: ")


# 크롬 드라이버 초기화
driver = webdriver.Chrome("C:/Users/rl/Desktop/py/chromedriver.exe")  

# 구글 검색 페이지 열기
driver.get("https://www.google.com")


pdf = "filetype:pdf "

#검색어 입력
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(pdf, keyword)
search_box.send_keys(Keys.ENTER)

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser') 
script1 = soup.select('div.bkWMgd > div.srg > div.g')

# PDF 파일 수집
pdf_links = []

while len(pdf_links) < quantity:
    links = driver.find_elements(By.XPATH, '//a')
    for link in links:
        href = link.get_attribute('href')
        if href and href.endswith('.pdf'):
            pdf_links.append(href)
            if len(pdf_links) == quantity:
                break

    if len(pdf_links) == quantity:
        break

    # 다음 페이지로 이동
    try:
        next_button = driver.find_element(By.ID, 'pnnext')
        next_button.click()
    except:
        break

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    # PDF 파일 다운로드
    for i, link in enumerate(pdf_links):
        response = requests.get(link,verify=False)
        file_name = f"{i+1}.pdf"  # 파일 이름 설정 방식을 변경할 수 있습니다.
        file_path = f"{save_path}/{file_name}"  # 저장 경로와 파일 이름을 조합합니다.
        with open(file_path, "wb") as file:
            file.write(response.content)


# 크롬 드라이버 종료
driver.quit()


