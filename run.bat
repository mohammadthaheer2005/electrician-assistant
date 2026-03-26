@echo off
cd /d %~dp0
call .venv\Scripts\activate
echo Starting Electrician Smart Assistant...
python -m streamlit run app.py
pause
