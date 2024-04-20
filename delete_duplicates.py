#-------------------------------------------------------------------------------
# Name:        delete duplicates
# Purpose: In case this bot publish duplicate products, you can execute this code to delete already published products from the main database
#
# Author:      Juan
#
# Created:     20/07/2023
# Copyright:   (c) Juan 2023
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
