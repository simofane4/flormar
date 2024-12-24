@echo off

:: Set the path to your virtual environment's activation script
set VENV_PATH=env\Scripts\activate

:: Check if the virtual environment exists
if not exist %VENV_PATH% (
    echo Virtual environment not found. Please ensure it's set up correctly.
    pause
    exit /b
)

:: Activate the virtual environment
call %VENV_PATH%

:: Inform the user
echo Virtual environment activated.

:: List of app names to create
set APPS=cart checkout core order products user_profile

:: Loop through each app name
for %%A in (%APPS%) do (
    echo Creating app %%A...
    python manage.py startapp %%A

    echo Adding serializers.py to %%A...
    echo.> %%A\serializers.py
    echo # Add your serializers here >> %%A\serializers.py

    echo App %%A and serializers.py created successfully!
)

:: Deactivate the virtual environment
deactivate

echo All apps created and serializers.py files added.
pause
