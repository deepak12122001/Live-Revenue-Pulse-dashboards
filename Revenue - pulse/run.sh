#!/bin/bash
echo "Starting Live Revenue Pulse Dashboard..."
streamlit run dashboard.py &
sleep 3
python generator.py &
echo "Both services started!"
echo "Dashboard will open in your browser"