@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..\..") do set "PROJECT_ROOT=%%~fI"
set "SCRIPT_PATH=%SCRIPT_DIR%normalizar_rgb_streaming.py"
set "RASTERIO_ENV_LOCAL=D:\Env\geo-raster-py311"
set "RASTERIO_ENV_SERVER=C:\Users\esrlrivero_adm\AppData\Local\ESRI\conda\envs\geo-raster-py311"
set "BAT_LOG_DIR=%SCRIPT_DIR%outputs\bat_logs"
if not exist "%BAT_LOG_DIR%" mkdir "%BAT_LOG_DIR%"
set "BAT_LOG=%BAT_LOG_DIR%\normalizar_rgb_streaming_ultimo.log"

if exist "%RASTERIO_ENV_LOCAL%\python.exe" (
    set "RASTERIO_PYTHON=%RASTERIO_ENV_LOCAL%\python.exe"
) else (
    set "RASTERIO_PYTHON=%RASTERIO_ENV_SERVER%\python.exe"
)
for %%I in ("%RASTERIO_PYTHON%") do set "RASTERIO_PREFIX=%%~dpI"
set "PATH=%RASTERIO_PREFIX%Library\bin;%RASTERIO_PREFIX%Scripts;%RASTERIO_PREFIX%DLLs;%RASTERIO_PREFIX%;%PATH%"
set "GDAL_DATA=%RASTERIO_PREFIX%Library\share\gdal"
set "PROJ_LIB=%RASTERIO_PREFIX%Library\share\proj"
set "PYTHONPATH="
set "PYTHONHOME="
set "GDAL_DRIVER_PATH="
set "CONDA_DLL_SEARCH_MODIFICATION_ENABLE=1"

echo ============================================================ > "%BAT_LOG%"
echo Inicio BAT: %DATE% %TIME% >> "%BAT_LOG%"
echo Proyecto: %PROJECT_ROOT% >> "%BAT_LOG%"
echo Python rasterio: %RASTERIO_PYTHON% >> "%BAT_LOG%"
echo Script Python: %SCRIPT_PATH% >> "%BAT_LOG%"

if not exist "%RASTERIO_PYTHON%" (
    echo ERROR: No se encontro Python rasterio: %RASTERIO_PYTHON%
    echo ERROR: No se encontro Python rasterio: %RASTERIO_PYTHON% >> "%BAT_LOG%"
    set "EXIT_CODE=1"
    goto FIN
)

if not exist "%SCRIPT_PATH%" (
    echo ERROR: No se encontro el script: %SCRIPT_PATH%
    echo ERROR: No se encontro el script: %SCRIPT_PATH% >> "%BAT_LOG%"
    set "EXIT_CODE=1"
    goto FIN
)

if "%~1"=="" (
    echo Uso:
    echo   normalizar_rgb_streaming.bat "RUTA\CARPETA_ENTRADA"
    echo.
    echo El script buscara TIFF recursivamente y escribira la salida en la carpeta normalizadas.
    echo ERROR: No se indico carpeta de entrada. >> "%BAT_LOG%"
    set "EXIT_CODE=1"
    goto FIN
)

set "EXTRA_ARGS=%*"

pushd "%PROJECT_ROOT%"
echo Opciones: %EXTRA_ARGS%
echo Opciones: %EXTRA_ARGS% >> "%BAT_LOG%"
echo Ejecutando normalizacion RGB streaming...
echo Ejecutando normalizacion RGB streaming... >> "%BAT_LOG%"
"%RASTERIO_PYTHON%" "%SCRIPT_PATH%" %EXTRA_ARGS% 1>> "%BAT_LOG%" 2>>&1
set "EXIT_CODE=%ERRORLEVEL%"
popd

:FIN
echo Fin BAT: %DATE% %TIME% >> "%BAT_LOG%"
echo Codigo salida: %EXIT_CODE% >> "%BAT_LOG%"
echo.
echo ===================== LOG DE EJECUCION =====================
type "%BAT_LOG%"
echo =================== FIN LOG DE EJECUCION ===================
echo.
echo Proceso finalizado con codigo: %EXIT_CODE%
echo Log BAT: %BAT_LOG%
echo Presione una tecla para cerrar esta ventana...
pause
exit /b %EXIT_CODE%
