# import pymysql.cursors
import datetime
# connection = pymysql.connect(host='localhost',
#                 			user='root',
#                  			password='cedric',
#                  			db='test',
#                  			charset='utf8mb4',
#                  			cursorclass=pymysql.cursors.DictCursor)

# with connection.cursor() as cursor:

# 	sql = "INSERT INTO `table1` VALUES (NULL, %s)"
# 	cursor.execute(sql, datetime.date(2016, 8, 14))
# connection.commit()


a = datetime.datetime(2016, 4, 12)
b = "19/04/2016"
#c = datetime.datetime.strptime(b, "%d/%m/%Y")
c = datetime.datetime.strftime(a, "%d-%m-%Y")
d = datetime.datetime.strptime(c, "%d-%m-%Y").date()
print(d)