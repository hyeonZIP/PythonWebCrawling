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


# 1분류를 선택하는 칸을 가리킴
field_LV1s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(1) > ul > li')
print(field_LV1s)
a = 1
for field_LV1 in field_LV1s:
    print(field_LV1.text)
    # 1분류 칸을 선택해서 드롭다운
    dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click()
    time.sleep(1)
    # 순차적으로 드롭다운 옵션을 차례대로 클릭함 > 해당 클릭을 통해 2분류가 동적으로 업데이트 됨 > 따라서 새롭게 크롤링을 해줘야 함
    dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[{a}]/a').click()
    # 새롭게 크롤링
    result_html = dr.page_source
    print(result_html)
    time.sleep(10)

    a += 1
    time.sleep(1)


# test = db.DB()
#
# sql = "SELECT * FROM users"
#
# test.save(sql)
