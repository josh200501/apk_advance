#! /bin/sh
ps -e |grep 'scrapy' > ~/pids
IFS="
"
for LINE in `cat ~/pids`
do
    #echo $LINE
    tmp=`echo "$LINE" |awk 'BEGIN{FS=" "}{print $1}'`
    echo $tmp
    echo "----------------"
    kill -9 $tmp
done
rm -f ~/pids
ps -e |grep 'python' > ~/pids
IFS="
"
for LINE in `cat ~/pids`
do
    #echo $LINE
    tmp=`echo "$LINE" |awk 'BEGIN{FS=" "}{print $1}'`
    echo $tmp
    echo "----------------"
    kill -9 $tmp
done
rm -f ~/pids
ps -e |grep 'wget' > ~/pids
IFS="
"
for LINE in `cat ~/pids`
do
    #echo $LINE
    tmp=`echo "$LINE" |awk 'BEGIN{FS=" "}{print $1}'`
    echo $tmp
    echo "----------------"
    kill -9 $tmp
done
rm -f ~/pids

