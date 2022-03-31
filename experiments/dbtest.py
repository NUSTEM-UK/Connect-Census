# pip3 install mysqlclient

import MySQLdb
from clientsecrets import username, password


db = MySQLdb.connect(host='localhost', user=username, passwd=password, db="pytest")

db.query("""select toyName, catDesc, toyPrice from NTL_special_offers inner join NTL_category on NTL_special_offers.catID = NTL_category.catID order by rand() limit 1""")

r = db.store_result()
print(r.fetch_row())
