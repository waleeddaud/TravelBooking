@echo off
echo ========================================
echo Travel Booking API - Performance Test
echo ========================================
echo.
echo Step 1: Ensure server is running on port 8000
echo Step 2: Running Locust tests...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Locust test
locust -f tests\performance\locustfile.py --host http://localhost:8000 --users 10 --spawn-rate 2 --run-time 20s --headless

echo.
echo ========================================
echo Test completed! Check results above.
echo ========================================
pause
