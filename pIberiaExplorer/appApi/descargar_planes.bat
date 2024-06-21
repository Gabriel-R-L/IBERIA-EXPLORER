@echo off
:CHECK_SERVER
echo Comprobar si el servidor Django esta activo
netstat -ano | findstr "127.0.0.1:8000"
IF %ERRORLEVEL% EQU 0 (
    echo El servidor esta activo, ejecutar scheduler.py
    set SCRIPT_DIR=%~dp0
    set PYTHON_SCRIPT=%SCRIPT_DIR%..\appApi\guardar_datos_api.py
    if exist "%PYTHON_SCRIPT%" (
        echo Ejecutando %PYTHON_SCRIPT%
        python "%PYTHON_SCRIPT%"
    ) else (
        echo No se encontro %PYTHON_SCRIPT%
        goto CHECK_SERVER
    )
    timeout /t 3600 /nobreak >nul
) ELSE (
    echo El servidor no esta activo, esperar unos segundos y volver a verificar
    timeout /t 5 /nobreak >nul
)
goto CHECK_SERVER

rem %0: Se refiere al nombre del archivo por lotes.
rem ~d: Modificador que extrae la letra de la unidad del archivo por lotes (por ejemplo, C:).
rem ~p: Modificador que extrae la ruta del archivo por lotes, excluyendo el nombre del archivo.
rem 0: Indica que se aplica al primer parámetro, que es el nombre del archivo por lotes.