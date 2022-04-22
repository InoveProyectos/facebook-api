# facebook-api

## Disposición de Directorios
```
.
├── api
│   ├── app.py
│   ├── templates
│   ├── static
│   ├── cfg
│   ├── routes
│   └── tools
├── docker
│   └── Dockerfile
├── docker-compose.yml
├── docs
├── Procfile
├── readme.md
└── requirements.txt
```
- `app.py`: Archivo main del proyecto
- `templates`: Archivos HTML
- `static`: Archivos CSS
- `cfg`: Archivos de configuración
- `routes`: Endpoints/Blueprints
- `tools`: Herramientas útiles para el proyecto
- `docker`: Archivos para construir contenedores de Docker
- `docs`: Documentación del código
- `requirements.txt`: Requerimientos necesarios
- `Procfile`: Archivo necesario para Deploy en Heroku

## Correr proyecto localmente
### Levantar Docker Containers
```bash
docker-compose up
```
### Iniciar una consola en Docker
```bash
docker exec -it flask-app bash
```

### Detener el proyecto
```bash
docker-compose stop
docker-compose down
```

## Deploy
Actualmente, en [Heroku](https://meta-apis-consumer.herokuapp.com)

# Formato mensajes de commit: [Semantic commits](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)