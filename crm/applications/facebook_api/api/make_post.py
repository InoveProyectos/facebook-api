#!/usr/bin/env python

from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated
from applications.facebook_api.classes.Facebook import Facebook


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def make_facebook_post(request):
    print(dict(request.POST))
    
    access_token = request.POST.get('access_token')
    page_id = request.POST.get('page_id')
    post_content = request.POST.get('content')
    tags = request.POST.get('tags')

    print('tags:', tags)
    hashtags = ''
    if tags:
        if ',' in tags:
            for tag in tags.split(','):
                hashtags += f'#{tag.strip()} '
        
        else:
            hashtags += f'#{tags.strip()}'    

    if not(access_token and page_id and post_content):
        return HttpResponse('Missing parameters', status=400)

    fb = Facebook(access_token, page_id)
    fb.make_post(post_content + '\n' + hashtags)

    return HttpResponseRedirect('/facebook/admin-page/' + page_id)
