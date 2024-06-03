@echo off
:CHECK_SERVER
echo Comprobar si el servidor Django esta activo
netstat -ano | findstr "127.0.0.1:8000"
IF %ERRORLEVEL% EQU 0 (
    echo El servidor esta activo, ejecutar scheduler.py
    python ..\api\guardar_datos_api.py
    timeout /t 3600 /nobreak >nul
) ELSE (
    echo El servidor no esta activo, esperar unos segundos y volver a verificar
    timeout /t 5 /nobreak >nul
)
goto CHECK_SERVER