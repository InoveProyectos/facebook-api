# Deploy en [Heroku]('heroku.com')

## Como es necesario que nuestro webhook esté en constante deploy, acá se aclara como funciona el deploy en heroku

#

## Requerimientos
```
gunicorn==20.0.1
```

#

## Procfile
Este archivo le indica a heroku como ejecutar la aplicación
```
web: gunicorn app:api/app.py
```

#
## Loguearse en heroku
```bash
heroku login
```

#

## Crear la aplicación en heroku y realizar deploy
```bash
git add .
git commit -am 'build: heroku deploy'
heroku create
```
Instantaneamente vamos a tener creada una aplicación en heroku, en este caso, el deploy está alojado
en `https://meta-apis-consumer.herokuapp.com/`

### Renombrar nuestra aplicación
```bash
heroku rename <NOMBRE>
```

### Para finalizar la subida de la app, es necesario pushear el código a Heroku
```bash
git push heroku master
```

### Listo! El servidor ya está funcionarlo, para apagarlo/encenderlo tenemos los comandos
```bash
heroku ps:scale web=0  # Apagar
heroku ps:scale web=1  # Encender
```

## Como hacer un deploy a heroku
1. Agregar archivos a subir
```bash
git add .
```

2. Realizar commit
```bash
git commit -am "build: heroku deploy"
```

3. Hacer push **a heroku master**
```bash
git push heroku master
```

## Levantar servidor
```bash
heroku ps:scale web=1
```

### Como apagar el servidor
```bash
heroku ps:scale web=0
```

## Observar logs de nuestra aplicación
```
heroku logs --tail
```