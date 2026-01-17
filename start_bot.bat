@echo off
chcp 65001 > nul 2>&1
title Telegram Schedule Bot
color 0A

cls
echo.
echo  ========================================
echo     TELEGRAM SCHEDULE BOT
echo  ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo  [X] Python не найден!
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo  [+] Создание requirements.txt...
    (
        echo python-telegram-bot^>=20.7
        echo python-dotenv==1.0.0
    ) > requirements.txt
)

if not exist "venv\" (
    echo  [+] Создание виртуального окружения...
    python -m venv venv >nul 2>&1
)

call venv\Scripts\activate.bat >nul 2>&1

pip install --upgrade pip --quiet >nul 2>&1
pip install --upgrade -r requirements.txt --quiet >nul 2>&1

if not exist ".env" (
    color 0E
    echo  [!] Файл .env не найден!
    echo  [+] Создание .env...
    echo BOT_TOKEN=YOUR_BOT_TOKEN_HERE > .env
    echo.
    echo  [!] Добавь токен в .env и перезапусти бота
    notepad .env
    pause
    exit /b 1
)

cls
echo.
echo  ========================================
echo     БОТ ЗАПУЩЕН
echo  ========================================
echo.
echo  [*] Бот работает...
echo  [*] Нажми Ctrl+C для остановки
echo.
echo  ========================================
echo.

python bot.py

if errorlevel 1 (
    color 0C
    echo.
    echo  ========================================
    echo     ОШИБКА ЗАПУСКА
    echo  ========================================
    echo.
    pause
) else (
    color 0E
    echo.
    echo  ========================================
    echo     БОТ ОСТАНОВЛЕН
    echo  ========================================
    echo.
    pause
)