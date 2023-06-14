from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
date2=[]
cont2 = []
nick2 = []
site2 = []
link_list=[]

try:
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')
    content_list = soup.find('ul', class_="lst_total")

    count = 0

    for i in content_list.find_all('li', "bx"):
        num2.append(num)
        print('번호:', num)
        num += 1

        link = i.find('a', class_='api_txt_lines total_tit')
        if link is not None:
            link_url = link['href']
            link_list.append(link_url)

    for link in link_list:
        driver.execute_script("window.open('{}', '_blank');".format(link))
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(2)

        frame = driver.find_element(By.ID, 'mainFrame')
        driver.switch_to.frame(frame)

        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        time.sleep(2)

        title = soup.find('div', class_='se-module se-module-text se-title-text').get_text()
        title2.append(title)
        print('제목:', title.strip())

        date = soup.find('span', class_='se_publishDate pcol2').get_text()
        date2.append(date)
        print('날짜:', date.strip())

        nick = soup.find('span', class_='nick').get_text()
        nick2.append(nick)
        print('닉네임:', nick.strip())

        cont = soup.find('div', class_='se-main-container').get_text()
        cont2.append(cont)
        print('내용:', cont.strip())

        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        time.sleep(2)

        site = i.find('a').get('data-url')
        site2.append(site)
        print('사이트:', site.strip())
        print('\n')

        count += 1
        if count >= input4:
            break

    result = pd.DataFrame()

    result['닉네임'] = nick2
    result['날짜'] = date2
    result['제목'] = title2
    result['내용'] = cont2
    result['사이트'] = site2

    
    
    with open(ft_name, 'a', encoding='UTF-8') as f:
        f.write('\n'.join(title2))
        f.write('\n')
        f.write('\n'.join(date2))
        f.write('\n')
        f.write('\n'.join(cont2))
        f.write('\n')
        f.write('\n'.join(nick2))
        f.write('\n')
        f.write('\n'.join(link_list))
        f.write('\n')

    result.to_csv(fc_name, encoding="utf-8-sig", index=False)
    result.to_excel(fx_name, index=False)

    driver.close()

except AttributeError:
    driver.quit()