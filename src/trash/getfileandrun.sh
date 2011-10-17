#!/bin/bash
HNURL="http://news.ycombinator.com"
DESTPATH="/home/skatenerd/Programs/python/hnproj/html/"
DATE=`date +%Y-%m-%d-%H`
FNAME="$DATE.txt"
DESTPATH="$DESTPATH$FNAME"
FUNNYPYSCRIPT="collect_data_from_page.py"
echo $DESTPATH
echo $FNAME
wget $HNURL -O $DESTPATH
python $FUNNYPYSCRIPT $FNAME
exit 0
