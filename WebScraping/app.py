import db
import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver  # 특정 url로 가상 웹페이지를 열어줌
from selenium.webdriver import ActionChains  # 액션체인 활성화(여러 개의 동작은 체인처럼 묶어서 저장, 실행 ex) 마우스 이동 클릭 키보드 등)

#240627
#페이지를 맨 처음에 로드를 하면 1분류가 랜덤으로 들어가있음



dr = webdriver.Chrome()  # C드라이브 windows 폴더에 드라이버 파일을 넣어두면 파일주소 지정을 안해줘도 됨
dr.get('https://datalab.naver.com/shoppingInsight/sCategory.naver')
result_html = dr.page_source

print(result_html)

act = ActionChains(dr)  # 크롬 드라이버에 동작을 실행시킬 명령어를 act로 지정

# 1. 지정할 요소를 선택
# 2. 해당 요소에 대한 동작 코드 작성

# element1 = dr.find_element_by_class_name('select_list scroll_cst')
# element1 = dr.find_element(By.CLASS_NAME, 'select_btn')

time.sleep(5)

soup = BeautifulSoup(result_html, 'html.parser')

a = 1
# 1분류를 선택하는 칸을 가리킴
field_LV1s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(1) > ul > li')
for field_LV1 in field_LV1s:
    print("1분류 : ",field_LV1.text)
    # 1분류 칸을 선택해서 드롭다운
    dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click()
    time.sleep(2)
    # 순차적으로 드롭다운 옵션을 차례대로 클릭함 > 해당 클릭을 통해 2분류가 동적으로 업데이트 됨 > 따라서 새롭게 크롤링을 해줘야 함
    dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[{a}]/a').click()
    a += 1
    time.sleep(2) # 너무 빨리 넘어가서 time sleep 으로 해결
    # 크롤링 부분@@@@
    result_html = dr.page_source
    soup = BeautifulSoup(result_html, 'html.parser')

    b = 1
    field_LV2s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(2) > ul > li')
    for field_LV2 in field_LV2s:
        print("2분류 : ", field_LV2.text)
        dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click()
        time.sleep(2)
        dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[{b}]/a').click()
        b += 1
        time.sleep(2)

        # 크롤링 부분@@@@
        result_html = dr.page_source
        soup = BeautifulSoup(result_html, 'html.parser')

        c = 1
        try:
            field_LV3s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(3) > ul > li')
            for field_LV3 in field_LV3s:
                print("3분류 : ", field_LV3.text)
                dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span').click()
                time.sleep(2)
                dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[{c}]/a').click()
                c += 1
                time.sleep(2)

                # 크롤링 부분@@@@
                result_html = dr.page_source
                soup = BeautifulSoup(result_html, 'html.parser')
                d = 1
                try:
                    print("4분류 검사 시작")
                    field_LV4s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(4) > ul > li')
                    for field_LV4 in field_LV4s:
                        print("4분류 : ", field_LV4.text)
                        dr.find_element(By.XPATH, '#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(4) > ul > li').click()
                        time.sleep(2)
                        dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[4]/ul/li[{d}]/a').click()
                        d += 1
                        time.sleep(2)

                        # 240627 4단계 까지 선택하는 곳 까지 함
                except:
                    print("4분류가 존재하지 않음")
                    continue
        except :
            print("3분류가 존재하지 않음")
            continue



    time.sleep(5)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@")


# test = db.DB()
#
# sql = "SELECT * FROM users"
#
# test.save(sql)
