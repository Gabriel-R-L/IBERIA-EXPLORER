<div style="display: flex; justify-content: center;">
<img src="pIberiaExplorer/static/favicon/android-chrome-384x384.png" alt="Iberia Explorer Logo" style="width: 250px; height: 250px;">
</div>


# Tabla de contenidos
1. [Pasos para preparar el proyecto](#1)
2. [Runnear el proyecto](#2)
3. [Notas dev](#3)
4. [Enlaces de interés](#4)
5. [Créditos](#5)


> [!IMPORTANT]  
> Es necesario tener Python 3.12.0 o superior instalado para que funcione correctamente 


## 1. Pasos para preparar el proyecto<a name="1"></a>
  - Clonar el repositorio  
  `git clone https://github.com/Gabriel-R-L/IBERIA-EXPLORER.git`    

  - Instalar dependencias (Python y NodeJS)  
  `pip install -r requirements.txt`
  `npm install`


**Ahora puedes hacer dos cosas: Importar un archivo .sql con datos, o realizar las migraciones y tener todo desde cero**


### Importar un archivo SQL
Antes de nada debes de saber que hay dos archivos de Base de Datos: `0001_iberiaexplorerdb.sql` y `iberiaexplorerdb.sql`  

* El primero contiene los datos más básicos para que el proyecto funcione sin problemas. Esto incluye los superusuarios (`gabrielramos@...` y `mariodelcampo@...`), así como contenido en tablas básicas (`Continentes`, `Ciudades`, etc).

* El segundo contiene lo que el archivo inicial tiene mas datos en otras tablas que se han usado para hacer pruebas.

*Si deseas esta opción, sigue estos pasos:*
> a) Acceder a psql con `psql -Upostgres`  
> b) Si no existe la DATABASE, `CREATE DATABASE iberiaexplorerdb;`
  - Si existe, `DROP DATABASE iberiaexplorerdb;` y la creamos
> c) `\q`  
> d) Situarse en la carpeta databases `cd databases`
> e) `psql -U postgres -d iberiaexplorerdb -f iberiaexplorerdb.sql`  

> [!NOTE]  
> El nombre del archivo puede variar dependiendo de cual quieras utilizar


### Hacer las migraciones y todo desde cero
> a) Ejecutar `py manage.py makemigrations`   
> b) Ejecutar `py manage.py migrate`   
> c) Crea un superusuario con `py manage.py createsuperuser`   


## 2. Runnear el proyecto<a name="2"></a>
Si los pasos anteriores los hemos hecho correctamente, simplemente con ejecutar `py manage.py runserver 8000` deberíamos poder ejecutar el proyecto de forma funcional.


## Notas dev<a name="3"></a>
### Exportar la Base de Datos
> a) Situarse en el directorio `databases`  
> b)`pg_dump -Upostgres iberiaexplorerdb > iberiaexplorerdb.sql` (o como quieras llamarlo)


## Enlaces de interés<a name="4"></a>
<a href="https://drive.google.com/drive/folders/18zmOZSqtcmCjDDGxGRwwFjBTBMriCVlX" target="_blank"><img src="https://img.shields.io/badge/Drive%20del%20TFG-blue?style=for-the-badge&logo=googledrive&logoColor=white"></a>


## Créditos<a name="5"></a>
<div style="display: flex; justify-content: center; gap:30px;">
<a href="https://github.com/Gabriel-R-L" target="_blank"><img src="https://avatars.githubusercontent.com/u/122472177?v=4" alt="Gabriel" style="width: 100px; height: 100px; border-radius: 50%;"></a>
<a href="https://github.com/palazMCA" target="_blank"><img src="https://avatars.githubusercontent.com/u/122304543?s=64&v=4" alt="Mario" style="width: 100px; height: 100px; border-radius: 50%;"></a>
</div>
