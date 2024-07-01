import mysql.connector

class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='49.247.13.181',
            port='3306',
            user='root',
            password='#zo240s!',
            database='sellit'
        )
        if self.connection.is_connected():
            print("sellit 테이블 연결 성공!!")
        else:
            print("sellit 연결 실패")
            exit(100)


    def select(self):
        cursor = self.connection.cursor()
        # 카테고리가 공백인 행 제거
        cursor.execute("SELECT iki_keyword, iki_category "
                       "FROM sellit_shop_item_keyword_info "
                       "WHERE iki_category != '' "
                       "LIMIT 500")
        return cursor.fetchall()

    def insert(self, keyword, year, month, click):
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO "
                       "sellit_shop_item_keyword_trend "
                       "VALUES(%s,%s,%s,%d)",keyword, year,month,click)
        return cursor.fetchall()

    def save(self, sql):
        #INSERT INTO sellit_shop_keyword_trend VALUES ()
        print("MySQL save 작업 " + sql)

# # 접속된 데이터베이스에서 쿼리 실행
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM result LIMIT 10")
# result = cursor.fetchall()
#
# # # 쿼리 결과 출력
# # for row in result:
# #     print(row)
#
# # 연결 종료
# cursor.close()
# connection.close()
#
# connection.close()
# exit(0)