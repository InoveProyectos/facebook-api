from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated

from applications.facebook_api.models import Page, Message
from applications.facebook_api.classes.Facebook import Facebook

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def answer_message(request):
    print(dict(request.POST))
    access_token = request.POST.get('access_token')
    page_id = request.POST.get('page_id')
    recv_id = request.POST.get('sender_id')
    message = request.POST.get('message')
    message_id = request.POST.get('message_id')

    print(access_token, page_id, recv_id, message, message_id)

    if not(access_token and page_id and recv_id and message and message_id):
        return HttpResponse('Missing parameters', status=400)

    fb = Facebook(access_token, page_id)
    fb.send_message(recv_id, message)

    # Aumentar el contador de mensajes respondidos de la página
    page = Page.objects.filter(page_id=int(page_id)).first()
    page.mensajes_respondidos += 1
    page.save()

    # eliminar mensaje de la db
    message_obj = Message.objects.get(id=int(message_id))
    message_obj.delete()

    return HttpResponseRedirect('/facebook/admin-page/' + page_id)
