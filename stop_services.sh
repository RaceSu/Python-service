#!/usr/bash
My_service = "Myservice"

num=`ps -ef | grep $My_service | wc -l`
if [ $num -gt "1" ]
then
	pid=`ps -ef | grep $id_service | sed -n '/python/p' | awk -F ' ' '{print $2}'`
	kill $pid
	echo "$id_service was stoped"
fi