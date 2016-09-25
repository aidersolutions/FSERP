#unused files
import psycopg2
import sys

password = raw_input("Please enter the password")
con = None
try:
    con = psycopg2.connect(database='testdb', host='localhost', user='tryton', password=password)
    con.set_isolation_level(0)
except Exception, e:
    print sys.exc_info()
if con:
    cursor = con.cursor()
    try:
        cursor.execute('drop schema public cascade')
    except Exception, e:
        print sys.exc_info()

    try:
        cursor.execute('crate schema public')
    except Exception, e:
        print sys.exc_info()

    try:
        cursor.commit()
    except Exception, e:
        print sys.exc_info()