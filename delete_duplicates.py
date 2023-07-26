#-------------------------------------------------------------------------------
# Name:        delete duplicates
# Purpose:
#
# Author:      rosit
#
# Created:     20/07/2023
# Copyright:   (c) rosit 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import psycopg2
from connectDB import connection
def main():
    con = connection()
    cur = con.cursor()
    query = """ DELETE FROM camperdata t1 USING camperdata t2 WHERE t1.id < t2.id AND t1.path = t2.path; SELECT path FROM camperdata; """
    cur.execute(query)
    data = cur.fetchall()

    # print the rows
    for row in data:
        print(row)

    cur.close()
    print("Query worked")
if __name__ == '__main__':
    main()
