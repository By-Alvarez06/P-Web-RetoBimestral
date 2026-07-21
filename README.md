# Plataformas Web - Reto Bimestral
## Integrantes: Byron Alvarez | Cody Cabrera

## Librerias necesarias para el funcionamiento del proyecto
```python
pip install -r requirements.txt
```
## Pasos para levantar el proyecto

### Levantar BD Postgres en contenedor Docker
```
docker compose up
```

### Iniciar proyecto Django
```python
python manage.py runserver
```

## Control de inicio de sesion y registro de usuarios
Django ofrece un Decorador para el control de unicio de sesion. 
Este protege fuciones verificando si el usuario esta autenticado, 
sin embargo la plataforma no tiene solo un tipo de usuario asi que se 
crea el archivo decorators.py en donde se verifica si el usuario esta 
autenticado y donde se sabe su rol.
