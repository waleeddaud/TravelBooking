#!/bin/bash
# Travel Booking API - Linux/Mac Startup Script

echo "========================================"
echo "Travel Booking API Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Check if dependencies are installed
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
    echo "Dependencies installed successfully!"
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Copying from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env file and set a secure SECRET_KEY"
    echo ""
fi

echo "Starting FastAPI server..."
echo ""
echo "API will be available at:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo "  - API Root: http://localhost:8000/"
echo ""
echo "Press CTRL+C to stop the server"
echo "========================================"
echo ""

# Set PYTHONPATH and start server
export PYTHONPATH=$(pwd)
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
