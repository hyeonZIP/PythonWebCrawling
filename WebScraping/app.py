from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import db
import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver  # 특정 url로 가상 웹페이지를 열어줌
from selenium.webdriver import ActionChains  # 액션체인 활성화(여러 개의 동작은 체인처럼 묶어서 저장, 실행 ex) 마우스 이동 클릭 키보드 등)

db_manager = db.DB()
categories = []
options = webdriver.ChromeOptions()
options.add_argument('--headless')      # 가상 크롬 창 띄우지 않고 돌리기
dr = webdriver.Chrome(options=options)  # C드라이브 windows 폴더에 드라이버 파일을 넣어두면 파일주소 지정을 안해줘도 됨
wait = WebDriverWait(dr, 10)    # 조건에 해당할 때까지 최대 10초 기다림
dr.get('https://datalab.naver.com/shoppingInsight/sCategory.naver')

act = ActionChains(dr)  # 크롬 드라이버에 동작을 실행시킬 명령어를 act로 지정

search_date = ((2023,1,2,3,4,5,6,7,8,9,10,11,12), (2024,1,2,3,4,5,6))
monthDb = ['01','02','03','04','05','06','07','08','09','10','11','12']

# 기간 > 월별
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/div'))).click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/ul/li[3]/a'))).click()

category_db_list = db_manager.select()
# DB 조회
case_counter = 0
for c in category_db_list:
    category_splited = []
    data_cid = ''

    # 구분자 탐색
    spliter = c[0].find('>')
    if spliter != -1:
        category_splited = c[0].split('>')
    else:
        category_splited.append(c[0])
    print(category_splited)

    # category 입력
    try:
        for j in range(len(category_splited)):
            for attempt in range(10):
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{j+1}]'))).click()
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{j+1}]/ul/*/a[text()="{category_splited[j]}"]'))).click()
                    break
                except Exception as e:
                    if attempt == 9:
                        raise e
                    print("분야 입력 재시도 : ", 9-attempt , "/ 10")
                    time.sleep(2)
        data_cid = dr.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{j+1}]/ul/*/a[text()="{category_splited[len(category_splited)-1]}"]').get_attribute('data-cid')
        print(data_cid)
    except Exception as e:
        print(e)
        print("category 입력 오류")
        continue

    # 검색 기간 설정 후 조회
    try:
        flag = True
        year_month_click = []
        # 날짜 선택, 조회, 그래프 탐색 진행
        for i in range(len(search_date)):
            year = search_date[i][0]
            month = search_date[i][1:]
            for attempt in range(10):
                try:
                    # 2023년도 선택, 조회 이후 2024년도를 선택하려면 end year부터 수정해야함
                    if flag:
                        # start year
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/ul/*/a[text()={year}]'))).click()
                        # start month
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/ul/*/a[text()={month[0]}]'))).click()
                        # end year
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[1]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[1]/ul/*/a[text()={year}]'))).click()
                        # end month
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]/ul/*/a[text()={month[len(month)-1]}]'))).click()
                        flag = False
                    else:
                        # end year
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[1]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[1]/ul/*/a[text()={year}]'))).click()
                        # end month
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[3]/div[2]/ul/*/a[text()={month[len(month)-1]}]'))).click()

                        # start year
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/ul/*/a[text()={year}]'))).click()
                        # start month
                        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]'))).click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/ul/*/a[text()={month[0]}]'))).click()
                    break
                except Exception as e:
                    print(e)
                    print("날짜 선택 오류")
                    if attempt == 9:
                        raise e
                    time.sleep(2)
            # 조회하기
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div/a'))).click()
            # 필수 대기 시간
            time.sleep(0.5)
            # 그래프 탐색
            for attempt in range(10):
                try:
                    insert_list = []
                    for n in month:
                        graph = wait.until(EC.presence_of_element_located((By.CLASS_NAME, f'bb-event-rect.bb-event-rect-{n-1}')))
                        act.move_to_element(graph).perform()
                        graph_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart1"]/div/div/div[1]/span')))
                        graph_value = dr.find_element(By.XPATH, '//*[@id="chart1"]/div/div/div[2]/span[3]')

                        if graph_date.text == '' or graph_value.text == '':
                            raise e
                        else:
                            year_month_click.append((year, monthDb[n-1], int(graph_value.text)))

                        print(graph_date.text)
                        print(graph_value.text)
                    print(year_month_click)
                    break
                except Exception as e:
                    if attempt == 9:
                        raise e
                    print("그래프 탐색 재시도 : ", 9-attempt , "/ 10")
                    time.sleep(2)

        # 최종 저장할 땐 ikc_no로 저장 >> c[1]
        for i in range(len(year_month_click)):
            try:
                db_manager.insert(data_cid, year_month_click[i][0], year_month_click[i][1], year_month_click[i][2])
            except Exception as e:
                print(e)
                print("저장 실패 : ", data_cid)

    except Exception as e:
        print(e)
        print("검색 기간 설정 후 조회 오류")

exit(400)