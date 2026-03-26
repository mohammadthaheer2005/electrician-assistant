@echo off
setlocal
echo ---------------------------------------------------
echo 🛠️ ELECTROASSIST VOICE FIXER 🛠️
echo ---------------------------------------------------
echo Phase 1: Installing standard dependencies...

pip install SpeechRecognition gTTS requests

echo.
echo Phase 2: Installing PyAudio (High-Speed Local Mic)...
pip install pyaudio

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Standard PyAudio install failed. Trying alternative (pipwin)...
    pip install pipwin
    pipwin install pyaudio
)

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Automated install failed. 
    echo Please follow these manual steps:
    echo 1. Go to: https://github.com/intx0h/pyaudio_wheels
    echo 2. Download the .whl for your Python version (run 'python --version' first).
    echo 3. Run: pip install [the_downloaded_file].whl
) else (
    echo.
    echo ✅ SUCCESS: Voice System is now ready! 
    echo Please RESTART your run.bat to activate changes.
)

pause
