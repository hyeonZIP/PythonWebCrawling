import mysql.connector

class DB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3307',
            user='admin',
            password='1234',
            database='item'
        )
        if self.connection.is_connected():
            print("MySQL 연결 성공!!")
        else:
            print("MySQL 연결 실패")
            exit(100)

    def save(self, sql):
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