# Following the Real Python database tutorial
# https://realpython.com/python-mysql/#creating-altering-and-dropping-a-table

from MySQLdb import connect, Error
from clientsecrets import username, password

try:
    with connect(
        host="localhost",
        user=username,
        # Password is already named correctly.
    ) as connection:
        create_db_query = "CREATE DATABASE online_movie_rating"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
            print("Database created successfully")

except Error as e:
    print("Error: ", e)

