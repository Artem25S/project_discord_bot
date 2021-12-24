chcp 65001
@echo off
@echo. 
echo Путь к файлам проекта: %~dp0
@echo. 

call %~dp0venv\Scripts\activate

cd %~dp0bot_packege

set TOKEN=OTIyMDY4NzI1NDA5MTQ0ODMz.Yb8Faw.hWmV_HE6mlYxiGYK0UA6V3F9LoI

python start_bot.py 

pause