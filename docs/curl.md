# Una guía basiquísima para usar cURL en el proyecto

### Siempre se empieza con `curl`

```bash
$ curl
```

## Peticiones de tipo POST

1. Para especificar el método de la petición, se usa la flag *(bandera)* `-X`, seguido del nombre del método **en mayúscula**
Ejemplo: Petición de tipo POST

```bash
$ curl -X POST
```

2. Como esta es una petición de tipo **POST**, suele tener un header, que se indica con `-H`

```bash
$ curl -X POST -H "Content-Type: application/json"
```

3. Además del Header, al realizar un post se tiene que indicar el valor de `data`, que se indica con `-d`

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"object": "page", "entry": [{"messaging": [{"message": "TEST_MESSAGE"}]}]}'
```

Listo!

## Peticiones de tipo GET

1. Para especificar el método de la petición, se usa la flag *(bandera)* `-X`, seguido del nombre del método **en mayúscula**
Ejemplo: Petición de tipo GET

```bash
$ curl -X GET
```

2. Luego, indicamos la url, con los parámetros dinámicos si se quiere
```bash

curl -X GET "https://una-pagina.com/endpoint?parametro1=valor1&parametro2=valor2"
```

Listo!