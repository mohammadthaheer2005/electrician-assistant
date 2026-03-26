@echo off
echo ---------------------------------------------------
echo 🛠️ ELECTROASSIST VOICE FIXER 🛠️
echo ---------------------------------------------------
echo Installing high-speed Local Mic dependencies...

pip install pyaudio SpeechRecognition

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Failed to install PyAudio automatically.
    echo.
    echo Try this instead:
    echo 1. Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio (or search for PyAudio wheels)
    echo 2. Download the .whl file for your Python version (e.g., cp311).
    echo 3. Run: pip install [filename].whl
    echo.
) else (
    echo.
    echo ✅ SUCCESS: Local Mic is now ready! 
    echo Please restart your run.bat to use the 'Mic' button.
)

pause
