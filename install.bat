@echo off
setlocal

:: Set the project directory path
set PROJECT_DIR=%cd%

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.x first.
    exit /b
)

:: Create a virtual environment (if not exists)
IF NOT EXIST "%PROJECT_DIR%\venv" (
    echo Creating virtual environment...
    python -m venv "%PROJECT_DIR%\venv"
)

:: Activate virtual environment
call "%PROJECT_DIR%\venv\Scripts\activate.bat"

:: Install required dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install tensorflow scikit-learn

:: Download and extract CIFAR-10 dataset
echo Downloading CIFAR-10 dataset...
python download_cifar10.py

:: Run the main Python script for CIFAR-10 image classification
echo Running the training script...
python cifar10_classifier.py

:: Deactivate virtual environment
deactivate

echo Done. The script has been executed successfully.

endlocal
pause
