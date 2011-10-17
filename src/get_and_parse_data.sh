#!/bin/bash
cd ~/Programs/python/hnproj/src
source ../bin/activate
HNURL="http://news.ycombinator.com"
DESTPATH="../html/"
DATE=`date +%Y-%m-%d-%H`
FNAME="$DATE.txt"
DESTPATH="$DESTPATH$FNAME"
FUNNYPYSCRIPT="collect_data_from_page.py"
echo $DESTPATH
echo $FNAME
wget $HNURL -O $DESTPATH
python $FUNNYPYSCRIPT $FNAME
exit 0
