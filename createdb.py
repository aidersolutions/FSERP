#unused files
import FSERP

import trytond
from trytond.config import config


config.update_etc('./FSERP/trytond/etc/trytond.conf')

from trytond.pool import Pool
from trytond.cache import Cache
from trytond.transaction import Transaction
from trytond.protocols import dispatcher

def db_exist(dbname):
    Database = trytond.backend.get('Database')
    database = Database().connect()
    cursor = database.cursor()
    databases = database.list(cursor)
    cursor.close()
    return dbname in databases


if __name__ == '__main__':
	dbname = 'testdb'
	if not db_exist(dbname):
		dispatcher.create(dbname, 'admin', 'en_US', 'root')
		print " db with name %s has been creted with server password admin and admin password root" % (dbname)
	else:
		print " db with name %s  already exists" %(dbname)
