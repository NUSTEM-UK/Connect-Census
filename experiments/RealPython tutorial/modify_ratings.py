from MySQLdb import connect, Error
from click import command
from clientsecrets import username, password

movie_id = input("Enter movie id: ")
reviewer_id = input("Enter reviewer id: ")
new_rating = input("Enter new rating: ")

update_query = """
UPDATE
    ratings
SET
    rating = %s
WHERE
    movie_id = %s AND reviewer_id = %s
"""
val_update_tuple = (
    new_rating,
    movie_id,
    reviewer_id,
)

check_query = """
SELECT *
FROM ratings
WHERE movie_id = %s AND reviewer_id = %s
"""
val_check_tuple = (
    movie_id,
    reviewer_id,
)

try:
    with connect (
        host="localhost",
        user=username,
        database="online_movie_rating",
    ) as connection:
        with connection.cursor() as cursor:
            result = cursor.execute(update_query, val_update_tuple)
            connection.commit()
            print(result)

            cursor.execute(check_query, val_check_tuple)
            result = cursor.fetchall()
            print(result)

except Error as e:
    print("Error: ", e)

