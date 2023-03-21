@echo off
ECHO Recuerde: este programa corre bajo python, debe estar instalado en la computadora.
ECHO El archivo a procesar debe encontrarse en la misma carpeta que 'graficar.py'
ECHO Al finalizar encontrara el grafico que se abrira fuera de esta carpeta.

SET /P DATOS=Archivo a procesar (sin extension):
SET /P SALIDA=Ingrese nombre archivo salida:
python graficar.py "%DATOS%.txt" "%SALIDA%"
echo Tarea finalizada.
IF EXIST "%SALIDA%".pkl DEL /F "%SALIDA%".pkl
echo Pulsa una tecla para salir
pause>nul
exit