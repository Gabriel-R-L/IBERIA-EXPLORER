# Iberia Explorer

## 1. Pasos a seguir para runnear el proyecto
  > a) Ejecutar `pip install -r requirements.txt`
  > b) Ejecutar `py manage.py makemigrations` 
  > c) Ejecutar `py manage.py migrate` 
  > d) Crea un superusuario con `py manage.py createsuperuser` 

## 2. Pasos para exportar la Base de Datos
  > a) `pg_dump -Upostgres iberiaexplorerdb > iberiaexplorerdb.sql`
  > b) Guardar en el directorio Databases

## 3. Pasos para importar la Base de Datos
  > a) Acceder a psql con `psql -Upostgres`
  > b) Si no existe la DATABASE, `CREATE DATABASE iberiaexplorerdb`
  > c) `\q`
  > c) `psql -Upostgres iberiaexplorerdb < iberiaexplorerdb.sql`
 
---
---
```
                Credits
                -------
Gabriel Ramos López y Mario del Campo Alves
               2023-2024
```
