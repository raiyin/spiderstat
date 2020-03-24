@echo off
set sum=1
set iter=0
:SUB1
set/A iter+=1
set/A sum=%iter% %% 2
if %sum% equ 1 (
c:\OSPanel\modules\database\MySQL-5.7-x64\bin\mysqldump --defaults-extra-file=c:\projects\spiderstat\backup\.sqlpwd -h 127.0.0.1 spyder_stat > e:\dump_0.sql & TIMEOUT /T 86400) else (
c:\OSPanel\modules\database\MySQL-5.7-x64\bin\mysqldump --defaults-extra-file=c:\projects\spiderstat\backup\.sqlpwd -h 127.0.0.1 spyder_stat > e:\dump_1.sql & TIMEOUT /T 86400
)
goto SUB1
