@echo off
REM Script de instalación para Multimedia Downloader en Windows
REM Autor: Kaelthar (ThornEldritch)

setlocal enabledelayedexpansion

REM Colores para Windows (usando caracteres especiales)
cls
echo.
echo ============================================================
echo   Multimedia Downloader - Script de Instalacion Windows
echo   Compatible: Windows 7, 8, 10, 11
echo   Autor: Kaelthar (ThornEldritch)
echo ============================================================
echo.

REM Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Este script requiere permisos de administrador.
    echo.
    echo Vuelve a ejecutar este archivo como administrador:
    echo  - Haz clic derecho en install.bat
    echo  - Selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

echo [INFO] Iniciando instalacion...
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python no encontrado en el PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Python encontrado: %PYTHON_VERSION%
echo.

REM Verificar pip
python -m pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] pip no encontrado
    echo Instalando pip...
    python -m ensurepip --upgrade
)

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] FFmpeg no encontrado
    echo.
    echo Para descargar video completo necesitas FFmpeg
    echo Descargalo desde: https://ffmpeg.org/download.html
    echo.
    echo O instala via:
    echo  - Chocolatey: choco install ffmpeg
    echo  - Scoop: scoop install ffmpeg
    echo.
    pause
)

REM Verificar git (opcional)
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Git no encontrado (opcional, no es necesario)
)

echo.
echo [INFO] Instalando dependencias Python...
echo.

REM Actualizar pip
python -m pip install --upgrade pip setuptools wheel

REM Instalar requirements
if exist requirements.txt (
    python -m pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo [!] Error instalando paquetes Python
        pause
        exit /b 1
    )
) else (
    echo [!] Archivo requirements.txt no encontrado
    pause
    exit /b 1
)

REM Crear directorios
echo.
echo [INFO] Creando directorios...

if not exist downloads (mkdir downloads)
if not exist logs (mkdir logs)
if not exist downloads\YouTube (mkdir downloads\YouTube)
if not exist downloads\TikTok (mkdir downloads\TikTok)
if not exist downloads\Instagram (mkdir downloads\Instagram)
if not exist downloads\Facebook (mkdir downloads\Facebook)
if not exist downloads\X (mkdir downloads\X)
if not exist downloads\Threads (mkdir downloads\Threads)
if not exist downloads\Pinterest (mkdir downloads\Pinterest)
if not exist downloads\Reddit (mkdir downloads\Reddit)
if not exist downloads\Vimeo (mkdir downloads\Vimeo)
if not exist downloads\SoundCloud (mkdir downloads\SoundCloud)
if not exist downloads\Otros (mkdir downloads\Otros)

echo [+] Directorios creados

REM Crear atajo de escritorio (opcional)
echo.
set /p CREATE_SHORTCUT="Deseas crear un acceso directo en el escritorio? (S/N): "
if /i "%CREATE_SHORTCUT%"=="S" (
    set "DESKTOP=%USERPROFILE%\Desktop"
    set "SCRIPT_PATH=%CD%\main.py"
    set "PYTHON_PATH=%PYTHON%"
    
    powershell -NoProfile -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Multimedia Downloader.lnk'); " ^
    "$Shortcut.TargetPath = 'python.exe'; " ^
    "$Shortcut.Arguments = '%SCRIPT_PATH% --help'; " ^
    "$Shortcut.WorkingDirectory = '%CD%'; " ^
    "$Shortcut.Save()"
    
    if %errorLevel% equ 0 (
        echo [+] Acceso directo creado en el escritorio
    )
)

echo.
echo ============================================================
echo   [+] Instalacion completada exitosamente!
echo ============================================================
echo.
echo Primeros pasos:
echo.
echo   1. Ver ayuda:
echo      python main.py --help
echo.
echo   2. Ver informacion del sistema:
echo      python main.py --system-info
echo.
echo   3. Descargar un video (ejemplo YouTube):
echo      python main.py -u "https://youtube.com/watch?v=..." --format best
echo.
echo   4. Extraer audio de un video:
echo      python main.py -u "https://youtube.com/watch?v=..." --audio
echo.
echo   5. Descargar desde un archivo de URLs:
echo      python main.py -f urls.txt --format best
echo.
echo ============================================================
echo.

pause
