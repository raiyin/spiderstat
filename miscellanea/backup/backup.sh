#!/bin/bash

for((i=1;i<101;i++))
do
  if [ `expr $i % 2` == 1 ]
  then
    mysqldump --defaults-extra-file=/home/pi/programs/spiderstat/miscellanea/backup/.sqlpwd -h localhost spyder_stat > /media/pi/disc/dump_0.sql
    sleep 24h
  else
    mysqldump --defaults-extra-file=/home/pi/programs/spiderstat/miscellanea/backup/.sqlpwd -h localhost spyder_stat > /media/pi/disc/dump_1.sql
    sleep 24h
  fi
done