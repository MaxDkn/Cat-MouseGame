@echo off
cls

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Erreur] : Vous devez installer Python !
    pause
    exit /b 1
)

:: Vérifier si Pygame est installé
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame n'est pas installé. Installation en cours...
    pip install pygame

)

start pythonw main.py
pause





