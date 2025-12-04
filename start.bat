@echo off
REM Travel Booking API - Windows Startup Script

echo ========================================
echo Travel Booking API Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Copying from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and set a secure SECRET_KEY
    echo.
)

echo Starting FastAPI server...
echo.
echo API will be available at:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo   - API Root: http://localhost:8000/
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Set PYTHONPATH and start server
set PYTHONPATH=%CD%
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

pause
