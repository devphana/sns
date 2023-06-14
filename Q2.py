from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import pandas as pd


input1 = input('1. 크롤링할 키워드는 무엇입니까?: ')
input2 = list(input('2. 포함할 키워드를 입력하세요: ').split())
input3 = list(input('3. 제외할 키워드를 입력하세요: ').split())
input4 = int(input('4. 크롤링할 건수는 몇 건입니까?: '))
input5 = input('5. 조회를 시작할 년도를 입력하세요(예:20220101): ')
input6 = input('6. 조회를 종료할 날짜를 입력하세요(예:20231014): ')
ft_name = input('7. txt 형태로 저장할 경로와 파일명을 확장자 포함해서 쓰세요(C:/Users/rl/Desktop/py/ex4.txt): ')
fc_name = input('8. csv 형태로 저장할 경로와 파일명을 확장자 포함해서 쓰세요(C:/Users/rl/Desktop/py/ex4.csv): ')
fx_name = input('9. xls 형태로 저장할 경로와 파일명을 확장자 포함해서 쓰세요(C:/Users/rl/Desktop/py/ex4.xls): ')


inckey = ' '.join(input2)
exckey = ' '.join(['-' + keyword for keyword in input3])
query = input1 + ' ' + inckey + ' ' + exckey


path = "C:/Users/rl/Desktop/py/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://www.naver.com")
time.sleep(2)


element = driver.find_element(By.ID, "query")
element.send_keys(query)
driver.find_element(By.ID, 'search-btn').click()


driver.find_element(By.LINK_TEXT, 'VIEW').click()


driver.find_element(By.LINK_TEXT, '블로그').click()


url = "https://search.naver.com/search.naver?where=blog&query={}&sm=tab_opt&nso=so:r,p:from{}to{}".format(query, input5, input6)
driver.get(url)

time.sleep(2)


num = 1
num2 = []
title2 = []
cont2 = []
nick2 = []
site2 = []

try:
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')
    content_list = soup.find('ul', class_="lst_total")

    count = 0
    for i in content_list.find_all('li', "bx"):
        num2.append(num)
        print('번호:', num)
        num += 1

        title = i.find('a', 'api_txt_lines total_tit').get_text()
        title2.append(title)
        print('제목:', title.strip())

        cont = i.find('div', 'api_txt_lines dsc_txt').get_text()
        cont2.append(cont)
        print('내용:', cont.strip())

        nick = i.find('a', 'sub_txt sub_name').get_text()
        nick2.append(nick)
        print('닉네임:', nick.strip())

        site = i.find('a').get('data-url')
        site2.append(site)
        print('사이트:', site.strip())
        print('\n')

        count += 1
        if count >= input4:
            break

    result = pd.DataFrame()

    result['번호'] = num2
    result['제목'] = title2
    result['내용'] = cont2
    result['닉네임'] = nick2
    result['사이트'] = site2

    with open(ft_name, 'a', encoding='UTF-8') as f:
        f.write('\n'.join(title2))
        f.write('\n')
        f.write('\n'.join(cont2))
        f.write('\n')
        f.write('\n'.join(nick2))
        f.write('\n')
        f.write('\n'.join(site2))
        f.write('\n')

    result.to_csv(fc_name, encoding="utf-8-sig", index=False)
    result.to_excel(fx_name, index=False)

except AttributeError:
    print("검색 결과가 없습니다.")