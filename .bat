@echo off
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Executando script Python...
python copag_monitor.py

echo.
pause
