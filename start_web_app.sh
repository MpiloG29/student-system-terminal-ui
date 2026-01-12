#!/bin/bash
echo "Ì∫Ä Starting Student Records Web Dashboard..."
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Ì≥¶ Installing Flask..."
    pip install flask
fi

echo "Ìºê Starting web server..."
echo "Ì≥ä Open your browser and go to: http://localhost:5000"
echo "Ìªë Press Ctrl+C to stop the server"
echo "=" * 50

python3 web_dashboard.py
