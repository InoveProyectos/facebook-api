from django.http import HttpResponse
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['GET', 'POST'])
@permission_classes([]) # No es necesario autenticación
def webhook(request):
    if request.method == 'GET':
        
        verify_token = 'inovevt' #os.getenv('VERIFY_TOKEN')

        # Parsear parametros recibidos por url
        mode = str(request.GET.get('hub.mode'))
        token = str(request.GET.get('hub.verify_token'))
        challenge = str(request.GET.get('hub.challenge'))

        # Verificar si token y mode fueron enviados en la petición
        if mode and token:

            # Verificar que mode y token coincidan con los valores esperados
            if mode == 'subscribe' and token == verify_token:

                # Enviar en la respuesta el token challenge que envió que llegó en request
                print(f'WEBHOOK_VERIFIED')
                return HttpResponse(challenge, status = 200)
            
        # 'Forbidden', ocurre cuando el token no coincide
        print(f'Tokens does not match')
        return HttpResponse(status = 403)
    
    elif request.method == 'POST':
        
        body = request.get_json()
        print(body) 

        if 'field' in body:
            if body.get('field') == 'feed':
                # Esto significa que nos llegó un webhook de la página
                return HttpResponse(status = 200)

        if body.get('object') == 'page':
            webhook_event = body.get('entry')[0].get('messaging')[0].get('message')
            print('Webhook event: ' + str(webhook_event))

            # Enviar una respuesta al mensaje

            recv_id = str(body.get('entry')[0].get('messaging')[0].get('sender').get('id'))
            
            message = 'Hola que tal! Dentro de las próximas horas vamos a ponernos en contacto con vos. :)'
            # fb.send_message(recv_id, message)

            # Return '200 OK' HttpResponse to all requests
            return HttpResponse('EVENT_RECEIVED', status = 200)

        # Returns a '404 Not Found' if event is not from a page subscription
        print(f'404 Not Found: {body}')
        return HttpResponse(status = 404)

    else:
        return HttpResponse(status = 404)
