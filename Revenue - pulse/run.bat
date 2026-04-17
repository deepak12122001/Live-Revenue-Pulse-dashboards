@echo off
echo Starting Live Revenue Pulse Dashboard...
start streamlit run dashboard.py
timeout /t 3
start python generator.py
echo Both services started!
echo Dashboard will open in your browser
pause