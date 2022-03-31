# pip3 install mysqlclient

from MySQLdb import _mysql
# from clientsecrets import username, password

# Alternative syntax would be:
# db = _myqsl.connect(host='localhost', db="pytest", read_default_file="~/.my.cnf")
# See https://dev.mysql.com/doc/refman/8.0/en/option-files.html
db = _mysql.connect(host='localhost', user='root', password='', database="pytest")

db.query("""select toyName, catDesc, toyPrice from NTL_special_offers inner join NTL_category on NTL_special_offers.catID = NTL_category.catID order by rand() limit 1""")

r = db.store_result()
print(r.fetch_row())
