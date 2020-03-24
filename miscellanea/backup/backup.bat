echo off
for /L %%B in (0,1,100) do (
if %%B%2==0	(
c:\OSPanel\modules\database\MySQL-5.7-x64\bin\mysqldump --defaults-extra-file=c:\projects\spiderstat\backup\.sqlpwd -h 127.0.0.1 spyder_stat > e:\dump_0.sql) & (
TIMEOUT /T 86400
) else	(
c:\OSPanel\modules\database\MySQL-5.7-x64\bin\mysqldump --defaults-extra-file=c:\projects\spiderstat\backup\.sqlpwd -h 127.0.0.1 spyder_stat > e:\dump_1.sql) & (
TIMEOUT /T 86400
)
echo %%B
)
