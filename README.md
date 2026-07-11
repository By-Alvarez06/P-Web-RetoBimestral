# Plataformas Web - Reto Bimestral
## Integrantes: Byron Alvarez | Cody Cabrera


## Librerias necesarias para la coneccion a la base de datos
pip install psycopg2-binary

## Control de inicio de sesion y registro de usuarios
Django ofrece un Decorador para el control de unicio de sesion. 
Este protege fuciones verificando si el usuario esta autenticado, 
sin embargo la plataforma no tiene solo un tipo de usuario asi que se 
crea el archivo decorators.py en donde se verifica si el usuario esta 
autenticado y donde se sabe su rol.