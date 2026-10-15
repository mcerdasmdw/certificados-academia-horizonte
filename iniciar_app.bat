@echo off
REM ============================================================
REM iniciar_app.bat - Lanza la app Flask de Academia Horizonte
REM Doble clic para ejecutar
REM ============================================================

echo.
echo ============================================================
echo   Academia Horizonte - Sistema de Certificados
echo   LA COCINA (Flask) iniciando...
echo ============================================================
echo.

REM Verificar que Python esté disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado en el PATH.
    echo Instala Python desde https://python.org y marca "Add to PATH".
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar que existan los archivos necesarios
if not exist "Insumos\Maestro_Estudiantes.xlsx" (
    echo ERROR: No se encuentra Insumos\Maestro_Estudiantes.xlsx
    pause
    exit /b 1
)

if not exist "Insumos\Registro_Evaluaciones.xlsx" (
    echo ERROR: No se encuentra Insumos\Registro_Evaluaciones.xlsx
    pause
    exit /b 1
)

if not exist "app.py" (
    echo ERROR: No se encuentra app.py
    pause
    exit /b 1
)

echo Iniciando servidor en http://localhost:5000
echo.
echo Para DETENER la app: presiona Ctrl+C en esta ventana
echo ============================================================
echo.

REM Ejecutar Flask
python app.py

REM Si el script termina, pausar para ver errores
echo.
echo La aplicacion se ha detenido.
pause