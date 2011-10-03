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
			contents=td.a.contents[0].__unicode__()
			contents=contents.encode("ascii","ignore")
			#have to watch out for the pesky "more link" at bottom of screen
			if (contents!='More'):
				url=td.a['href'].encode('ascii','ignore')
				links.append({"title":contents,"url":url})
	return links

def parseSubtext(children):
	pts_str=children[0].contents[0]
	pts=pts_str.split()[0]
	pts=int(pts)
	user=children[1].contents[0].__unicode__()
	user=user.encode("ascii","ignore")
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

def getEntries():
	sys.path.append('../html')
	f=open('../html/sampleHN.html', 'r')
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
		entries.append(curDict)
	return entries

def getQueryStr(entry, pg_obj, table_name):
	qstr="INSERT INTO "+table_name+" "
	qstr+="("
	qstr+=", ".join(entry.keys())
	qstr+=") "
	qstr+="VALUES ("
	#i should probabl groom the values elsewhere
	qstr+=", ".join(map(groom_for_query_str, entry.values()))
	qstr+=")"
	return qstr


def groom_for_query_str(val):
	if (isinstance(val,unicode)):
		raise CustomException("Encoding error.  nothing should ever be unicode")
	val=enquote_if_str(val)
	val=str(val)
	return val


def enquote_if_str(val):
	if(isinstance(val,str)):
		return "$$"+val[:98]+"$$"
	else:
		return val


if __name__ == "__main__":
	from BeautifulSoup import BeautifulSoup
	import pg
	import sys

	debug=True

	#connect to:
	#database=HNDB
	#table=hnposts
	#password=foo
	db_name="HNDB"
	host_name="localhost"
	table_name="hnposts"
	db_passwd="foo"
	
	pg_obj=pg.connect(dbname=db_name, host=host_name, passwd=db_passwd)

	entries = getEntries()
	for e in entries:
		query_str=getQueryStr(e,pg_obj,table_name)
		if debug:
			print query_str
		pg_obj.query(query_str)
	if debug:
		print pg_obj.query("select * from hnposts")
		getQueryStr(dummy_entry,pg_obj)
