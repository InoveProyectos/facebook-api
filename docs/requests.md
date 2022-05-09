# Requests a nuestra API

## Para Testing

## **GET - `/webhook`**
```bash
curl -X GET "https://inove-facebook-api.herokuapp.com/webhook?hub.verify_token=VERIFY_TOKEN&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe"
```

## **POST - `/webhook`**
```bash
curl -H "Content-Type: application/json" -X POST "https://inove-facebook-api.herokuapp.com/webhook" -d '{"object": "page", "entry": [{"messaging": [{"message": "TEST_MESSAGE"}]}]}'
```

# Requests a GRAPH API

## Get page ID

### Necesario
- `user access token` (Administrador de la página)
```bash
curl -i -X GET "https://graph.facebook.com/{user-id}/accounts
     ?access_token={user-access-token}"
```

## Get access token

### Necesario:
- `user access token` (Administrador de la página)
- `PAGE_ID` (Ver item anterior)
```bash
curl -i -X GET "https://graph.facebook.com/PAGE-ID?
  fields=access_token&
  access_token=USER-ACCESS-TOKEN"
```