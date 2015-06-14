#!/bin/bash

stty -F /dev/$1 speed 9600 cs8 -cstopb -parenb -echo
while true
do
	while read p
	do
		line=""
		for (( i=0; i<${#p}; i+=2 ))
		do
			line=$line"\\x"${p:$i:2}
		done
		echo $line
		echo -en $line > /dev/$1
		sleep 3
	done < $2
done


