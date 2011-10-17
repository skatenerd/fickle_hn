from BeautifulSoup import BeautifulSoup
import pgdb
import sys


def extended_list(t):
	rtnVal=[]
	for x in t:
		rtnVal.extend(x)
	return rtnVal

def get_links(soup_doc):
	titleTDs=soup_doc.findAll('td', {'class': 'title'})
	links=[]
	for td in titleTDs:
		if td.a!=None:
			#risky figure this out
			contents=str(td.a.contents[0])
			#have to watch out for the pesky "more link" at bottom of screen
			if (contents!='More'):
				url=td.a['href']
				links.append({"title":contents,"url":url})
	return links

def parseSubtext(children):
	pts_str=children[0].contents[0]
	pts=pts_str.split()[0]
	pts=int(pts)
	user=str(children[1].contents[0])
	comments_str=children[2].contents[0]
	comments_arr=comments_str.split()
	comments=0
	if len(comments_arr)>1:
		comments=int(comments_arr[0])
	else:
		commments=0
	return{"score":pts,"username":user,"comments":comments}




def get_subtexts(soup_doc):
	subtextTDs=soup_doc.findAll('td',{'class':'subtext'})
	subtexts=[]
	for td in subtextTDs:
		children=td.findChildren()
		if len(children)==3:
			subtextTuple=parseSubtext(children)
			subtexts.append(subtextTuple)
		else:
			raise CustomException("Parse error: subtext has children != 3")
	return subtexts

def getEntries(fname):
	sys.path.append('../html')
	f=open('../html/'+fname, 'r')
	data_str="".join(f)
	soup_doc=BeautifulSoup(data_str)
	links=get_links(soup_doc)
	subtexts=get_subtexts(soup_doc)
	
	numLinks=len(links)
	numSubtexts=len(subtexts)
	if numLinks!=numSubtexts:
		raise CustomException("Parse error: numsubtexts!=numlinks")
	else:
		numEntries=numLinks

	entries=[]
	for i in range(numEntries):
		curDict={}
		curDict.update(links[i])
		curDict.update(subtexts[i])
		vals=curDict.values()
		groomed_vals=map(groom_for_query_str,vals)
		entries.append(tuple(groomed_vals))
	return entries



def groom_for_query_str(val):
	if (isinstance(val,unicode)):
		val=val.encode('ascii','ignore')

	if(not isinstance(val,str)):
		val=str(val)
	return val[:100]




if __name__ == "__main__":
	debug=True

	#connect to:
	#database=HNDB
	#table=hnposts
	#password=foo
	db_name="HNDB"
	host_name="localhost"
	table_name="hnposts"
	db_passwd="foo"
	fname=sys.argv[1]
	
	pg_obj=pgdb.connect(dsn=host_name+":"+db_name, password=db_passwd)
	insert_cursor=pg_obj.cursor()

	entries = getEntries(fname)
#	for e in entries:
#		query_str=getQueryStr(e,pg_obj,table_name)
#		if debug:
#			print query_str
#		pg_obj.query(query_str)
#	print entries[0].keys()

	insert_cursor.executemany("insert into "+table_name+"(url, username,score,comments,title,timestamp) VALUES (%s,%s,%s,%s,%s,now())",entries)
	insert_cursor.execute("select * from "+table_name)
	#insert_cursor.execute("truncate table hnposts")
	pg_obj.commit()
	#print insert_cursor.fetchall()
	#print insert_cursor.rowcount
	insert_cursor.close()
	pg_obj.close()
