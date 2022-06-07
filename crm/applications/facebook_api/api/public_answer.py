from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated

from applications.facebook_api.models import Page
from applications.facebook_api.classes.Facebook import Facebook

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def answer_comment(request):
    access_token = request.POST.get('access_token')
    page_id = request.POST.get('page_id')
    post_id = request.POST.get('post_id')
    message = request.POST.get('message')

    if not(access_token and page_id and post_id and message):
        return HttpResponse('Missing parameters', status=400)

    fb = Facebook(access_token, page_id)
    fb.comment(post_id, message)
    fb.put_like(post_id)

    # Aumentar el contador de post respondidos de la página
    page = Page.objects.filter(page_id=int(page_id)).first()
    page.posts_respondidos += 1
    page.save()

    return HttpResponseRedirect('/facebook/admin-page/' + page_id)
