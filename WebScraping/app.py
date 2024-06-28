from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import db
import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver  # 특정 url로 가상 웹페이지를 열어줌
from selenium.webdriver import ActionChains  # 액션체인 활성화(여러 개의 동작은 체인처럼 묶어서 저장, 실행 ex) 마우스 이동 클릭 키보드 등)

dr = webdriver.Chrome()  # C드라이브 windows 폴더에 드라이버 파일을 넣어두면 파일주소 지정을 안해줘도 됨
wait = WebDriverWait(dr, 10)
# element = wait.until(EC.element_to_be_)
dr.get('https://datalab.naver.com/shoppingInsight/sCategory.naver')
result_html = dr.page_source

act = ActionChains(dr)  # 크롬 드라이버에 동작을 실행시킬 명령어를 act로 지정

# 1. 지정할 요소를 선택
# 2. 해당 요소에 대한 동작 코드 작성

# element1 = dr.find_element_by_class_name('select_list scroll_cst')
# element1 = dr.find_element(By.CLASS_NAME, 'select_btn')

time.sleep(1)

soup = BeautifulSoup(result_html, 'html.parser')

total_test_item = 0

# 기간을 월간으로 변경
dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/span').click()
dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/ul/li[3]/a').click()
dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/span/label[3]').click()

a = 1
# 1분류를 선택하는 칸을 가리킴
field_LV1s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(1) > ul > li')
for field_LV1 in field_LV1s:
    # 1분류 칸을 선택해서 드롭다운
    dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span').click()
    # 순차적으로 드롭다운 옵션을 차례대로 클릭함 > 해당 클릭을 통해 2분류가 동적으로 업데이트 됨 > 따라서 새롭게 크롤링을 해줘야 함
    dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[{a}]/a').click()
    print("1분류 : ",field_LV1.text)
    a += 1
    time.sleep(0.5) # 너무 빨리 넘어가서 time sleep 으로 해결

    # 크롤링 부분@@@@
    result_html = dr.page_source
    soup = BeautifulSoup(result_html, 'html.parser')

    b = 1 ## 2분류
    field_LV2s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(2) > ul > li')
    for field_LV2 in field_LV2s:
        dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span').click()
        dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li[{b}]/a').click()
        print("2분류 : ", field_LV2.text)
        b += 1
        time.sleep(0.5) # 필수

        # 크롤링 부분@@@@
        result_html = dr.page_source
        soup = BeautifulSoup(result_html, 'html.parser')
        c = 1

        field_LV3s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(3) > ul > li')
        if field_LV3s:
            for field_LV3 in field_LV3s:
                dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/span').click()
                dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li[{c}]/a').click()
                print("3분류 : ", field_LV3.text)
                c += 1
                time.sleep(0.5) # 필수

                # 크롤링 부분@@@@
                result_html = dr.page_source
                soup = BeautifulSoup(result_html, 'html.parser')

                d = 1
                field_LV4s = soup.select('#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(4) > ul > li')
                if field_LV4s:
                    for field_LV4 in field_LV4s:
                        dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[4]/span').click()
                        dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[4]/ul/li[{d}]/a').click()
                        print("4분류 : ", field_LV4.text)
                        d += 1
                        # 조회 버튼 클릭
                        dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click()
                        time.sleep(0.5) #필수

                        total = 0
                        for i in range(12):
                            # graph = dr.find_element(By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')
                            graph = wait.until(EC.presence_of_element_located((By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')))
                            act.move_to_element(graph).perform()
                            act.reset_actions()

                            graph_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart1"]/div/div/div[1]/span')))
                            # graph_date = dr.find_element(By.XPATH, '//*[@id="chart1"]/div/div/div[1]/span')
                            graph_value = dr.find_element(By.XPATH, '//*[@id="chart1"]/div/div/div[2]/span[3]')

                            total += int(graph_value.text)

                            print(graph_date.text)
                            print(graph_value.text)
                        total_test_item += 1
                        print("테스트 케이스 : ", total_test_item)
                        print("합계 : ", total)
                        print("평균 : ", total/12)
                        print("===================================================================================================")

                else:
                    # 조회 버튼 클릭
                    dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click()
                    time.sleep(0.5) #필수, 0.1~0.3으로 하면 에러

                    total = 0
                    for i in range(12):
                        # graph = dr.find_element(By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')
                        graph = wait.until(EC.presence_of_element_located((By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')))
                        act.move_to_element(graph).perform()

                        graph_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart1"]/div/div/div[1]/span')))
                        graph_value = dr.find_element(By.XPATH, '//*[@id="chart1"]/div/div/div[2]/span[3]')

                        total += int(graph_value.text)

                        print(graph_date.text)
                        print(graph_value.text)
                    act.reset_actions()
                    total_test_item += 1
                    print("테스트 케이스 : ", total_test_item)
                    print("합계 : ", total)
                    print("평균 : ", total/12)
                    print("===================================================================================================")
        else:
            #조회 버튼 클릭
            dr.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a').click()
            time.sleep(0.5) #필수, 0.1~0.3으로 하면 에러

            total = 0
            for i in range(12):
                # graph = dr.find_element(By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')
                graph = wait.until(EC.presence_of_element_located((By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')))
                act.move_to_element(graph).perform()
                act.reset_actions()

                graph_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart1"]/div/div/div[1]/span')))
                graph_value = dr.find_element(By.XPATH, '//*[@id="chart1"]/div/div/div[2]/span[3]')

                total += int(graph_value.text)

                print(graph_date.text)
                print(graph_value.text)
            total_test_item += 1
            print("테스트 케이스 : ", total_test_item)
            print("합계 : ", total)
            print("평균 : ", total/12)
            print("===================================================================================================")

# test = db.DB()
#
# sql = "SELECT * FROM users"
#
# test.save(sql)
