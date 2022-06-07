#!/usr/bin/env python

from django.http import HttpResponse
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import redirect
from django.contrib.auth.models import User

from applications.facebook_api.models import Page, Response

import sys, os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_answer(request):
    
    # ID de la página (FK), NO ID de Facebook
    page_id = request.POST.get('id')
    
    tag = request.POST.get('tag')
    message = request.POST.get('message')

    if not(page_id and tag and message):   
        print('No se recibieron todos los datos necesarios')    
        return HttpResponse(status = 400, content = 'Bad request')

    try:

        page_obj = Page.objects.get(id = page_id)
        
        if not page_obj:

            return HttpResponse(status = 400, content = 'Bad request, no se encontró la página')

        response_obj = Response.objects.create(page = page_obj, tag = tag, message = message)
        response_obj.save()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return HttpResponse(status = 400, content = f'Bad request: {e}')
    
    return redirect('admin-page/' + str(page_obj.page_id))
