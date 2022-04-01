# pip3 install mysql-connector-python
# THis is the official database connector, but it's pure python and hence slow.
# Good tutorial here, though:
# https://realpython.com/python-mysql/

from mysql.connector import connect, Error
import clientsecrets

try:
    # Context manager obviates need to close connection
    with connect(
        host="localhost",
        user=clientsecrets.username,
        password=clientsecrets.password,
        database="pytest",
    ) as connection:
        # print(connection)
        db_query = "select toyName, catDesc, toyPrice from NTL_special_offers inner join NTL_category on NTL_special_offers.catID = NTL_category.catID order by rand() limit 1"
        with connection.cursor() as cursor:
            cursor.execute(db_query)
            result = cursor.fetchall()
            print(result)
except Error as e:
    print(e)

