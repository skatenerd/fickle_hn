import pgdb


#connect to:
#database=HNDB
#table=hnposts
#password=foo
db_name="HNDB"
host_name="localhost"
table_name="hnposts"
db_passwd="foo"

def open_conn():
	"""return (connection_obj,cursor)"""
	pg_obj=pgdb.connect(dsn=host_name+":"+db_name, password=db_passwd)
	return pg_obj

def viewdb(pg_obj):
	view_cursor=pg_obj.cursor()
	view_cursor.execute("select * from "+table_name)
	print view_cursor.fetchall()
	print view_cursor.rowcount
	view_cursor.close()

def cleardb(pg_obj):
	clearing_cursor=pg_obj.cursor()
	clearing_cursor.execute("truncate table hnposts")
	pg_obj.commit()
	clearing_cursor.close()

def closedb(pg_obj):
	pg_obj.close()

