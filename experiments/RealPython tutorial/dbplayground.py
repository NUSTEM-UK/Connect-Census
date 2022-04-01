# pip3 install mysqlclient

import MySQLdb
from clientsecrets import username, password


db = MySQLdb.connect(host='localhost',
                     user=username,
                     passwd=password,
                     db="menu")

cursor = db.cursor()

cursor.execute('select * from fish')
# print(command)
results = cursor.fetchall()
for record in results:
    print(record[0], "-->", record[1], " @", record[2])


cursor.execute("""select * from fish where name LIKE '%s'""" %("tuna"))
results = cursor.fetchall()
for record in results:
    print(record[0], "-->", record[1], " @", record[2])
