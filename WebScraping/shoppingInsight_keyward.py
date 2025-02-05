import traceback
import re
import db
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver  # 특정 url로 가상 웹페이지를 열어줌
from selenium.webdriver import ActionChains  # 액션체인 활성화(여러 개의 동작은 체인처럼 묶어서 저장, 실행 ex) 마우스 이동 클릭 키보드 등)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

total_count = 0
test = db.DB()
result = test.select()
keywords = []
categories = []

for row in result:
    #DB에 공백이 있을 경우 SELECT 할 때 '\xa0' 이 출력됨
    # 공백 -(대쉬) ,(쉼표) .(온점) ･(모바일 ･) `(아래따옴표) '(따옴표)
    k = row[0]
    if k != '':
        keywords.append(k)
        c = row[1]
        # 카테고리 마지막에 공백 있을 시 마지막 공백만 제거
        if c and c[-1] == ' ':
            c = c[:len(c)-1]+c[-1].replace(' ', '')
        categories.append(c)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
dr = webdriver.Chrome(options=options)  # C드라이브 windows 폴더에 드라이버 파일을 넣어두면 파일주소 지정을 안해줘도 됨
wait = WebDriverWait(dr, 5)
dr.get('https://datalab.naver.com/shoppingInsight/sKeyword.naver')
result_html = dr.page_source
act = ActionChains(dr)
soup = BeautifulSoup(result_html, 'html.parser')

# 최대 연속된 12개월 데이터 검색 가능 ex) 2023 06 ~ 2024 07
# 안되는 범위 ex) 1월 5월 7월 검색 X / 2023 01 ~ 2024 12 X / 한 키워드로 조회를 2번해야하는 경우 전부 불가능
start_year = '2023'
start_month = '01'
end_year = '2023'
end_month = '12'
# monthDb는 데이터베이스에 저장할 때 문자로 넣어야함으로 야매?로 지정
monthDb = ['01','02','03','04','05','06','07','08','09','10','11','12']

# 기간 > 월간
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div/ul/li[3]/a'))).click()
# 연도 > 2023~
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[1]/div[1]'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[1]/div[1]/ul/*/a[text()={start_year}]'))).click()
# 월 > 01~
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[1]/div[2]'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[1]/div[2]/ul/*/a[text()={start_month}]'))).click()
# 연도 > ~2023
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[3]/div[1]'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[3]/div[1]/ul/*/a[text()={end_year}]'))).click()
# 월 > ~12
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[3]/div[2]'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[3]/div[2]/span[3]/div[2]/ul/*/a[text()={end_month}]'))).click()

# print(soup)
for i in range(len(keywords)):

    #구분자 탐색
    spliter = categories[i].find('>')
    if(spliter != -1):
        category = categories[i].split('>')
    else:
        category = categories[i].split(' ')

    keyword = keywords[i]

    print(category)
    print(keyword)

    # 분야별 입력
    try:
        for j in range(len(category)):
            for attempt in range(10):
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{j+1}]'))).click()
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{j+1}]/ul/*/a[text()="{category[j]}"]'))).click()
                    break
                except:
                    print("분야 입력 재시도 중 : ", 9-attempt , "/ 10")
                    if attempt == 9:
                        raise e
                    time.sleep(2)
    except Exception as e:
        print(e)
        print("category : ", category)
        print("keyword : ", keyword)
        print("분야별 선택 오류")
        print(traceback.format_exc())
        continue

    # 키워드 입력
    try:
        for attempt in range(10):
            try:
                dr.find_element(By.XPATH, '//*[@id="item_keyword"]').send_keys(keyword)
                # 조회
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a'))).click()
                break
            except:
                print("키워드 입력 재시도 중 : ", 9-attempt , "/ 10")
                if attempt == 9:
                    raise e
                time.sleep(1)
                keywordDeleteBtn = dr.find_elements(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/a')
                if keywordDeleteBtn:
                    keywordDeleteBtn[0].click()
                time.sleep(1)
    except Exception as e:
        print(e)
        print("category : ", category)
        print("keyword : ", keyword)
        print("키워드 입력 및 조회 오류")
        print(traceback.format_exc())
        continue

    time.sleep(0.5) # 필수 대기 시간
    # 그래프 탐색
    try:
        for attempt in range(10):
            try:
                total = 0
                click = []
                for i in range(12):
                    graph = wait.until(EC.presence_of_element_located((By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{i}')))
                    act.move_to_element(graph).perform()
                    graph_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart1"]/div/div/div[1]/span')))
                    graph_value = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart1"]/div/div/div[2]/span[3]')))
                    if graph_date.text == '' or graph_value.text == '':
                        raise e
                    else:
                        total += int(graph_value.text)
                        click.append(int(graph_value.text))
                        # print("연도:", start_year , "월:", month[0], "클릭수:", graph_value.text)
                        # test.insert(start_year, graph_date.text, graph_value.text)
                # print("총 클릭 수 : ",total)
                if total >= 100:
                    print("DB저장")
                    for j in range(12):
                        # print(keyword, start_year, monthDb[i], click[i])
                        try:
                            test.insert(keyword, start_year,monthDb[j], click[j])
                        except Exception as e:
                            print(e)

                else:
                    print("저장하지 않음")
                total_count += 1
                print("case : ", total_count)
                break
            except:
                print("그래프 탐색 재시도 중 : ", 9-attempt , "/ 10")
                if attempt == 9:
                    raise e
                time.sleep(2)
    except Exception as e:
        print(e)
        print("category : ", category)
        print("keyword : ", keyword)
        print("그래프 탐색 오류")
        print(traceback.format_exc())

    # 삭제
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/a'))).click()

quit(400)