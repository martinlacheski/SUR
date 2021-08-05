# Sistema Unificado para Rectificadoras (S.U.R.)

Trabajo Final Analista en Sistemas de Computación
Universidad Nacional de Misiones - Argentina

# BASE DE DATOS:

Inicialmente se utiliza la BD por defecto de Django, SQLITE3.
Para etapas mas avanzadas del proyecto utilizaremos PostgreSQL 12.7

# ENTORNO VIRTUAL del Proyecto

Crear un entorno virtual al nivel de la carpeta app con el siguiente comando:

python3 -m venv venv

Luego acceder a "RAIZ Proyecto"/venv/bin y ejecutar:

source bin/ activate #Para activar el entorno virtual

# LIBRERIAS NECESARIAS del Proyecto

Luego ejecutar lo siguiente para instalar las librerias necesarias:

pip install Django==3.2.6 #Para instalar django en el entorno virtual 
pip install django-widget-tweaks==1.4.8 #Libreria necesaria para el proyecto.
pip install Pillow==8.3.1 #Para poder utilizar imagenes en el proyecto

Otra alternativa es en vez de ejecutar lo anterior, podemos ejecutar el comando siguiente en la terminal, despues de activado el entorno virtual:

En la carpeta raiz del proyecto ejecutamos:

pip install -r requirements.txt

# Crear Superusuario

Ubicarse dentro de la carpeta app/

Ejecutar el siguiente comando:

python3 manage.py createsuperuser

Seguir los pasos para poder crear un usuario.

# Ejecutar el Proyecto

Ubicarse dentro de la carpeta app/

Ejecutar el siguiente comando:

python3 manage.py runserver

Luego acceder a:

http://127.0.0.1:8000


El proyecto fue realizado con las siguiente tecnologías:

Python 3.8.10 -- Django 3.2.6 -- Bootstrap 5.1.0 -- Template AdminLTE 3.1.0
