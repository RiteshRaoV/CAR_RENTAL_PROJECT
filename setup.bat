@echo off
REM Create a virtual environment named .venv
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip to the latest version
python -m pip install --upgrade pip

REM Install Django
pip install django

REM Install mysqlclient
pip install mysqlclient

pip install drf-yasg

pip install djangorestframework

pip install pillow

echo Django installation complete. The virtual environment is activated.
pause
