#!/usr/bin/env python

from django.urls import path
from applications.facebook_api.api.credentials import *
from applications.facebook_api.api.webhook import webhook
from applications.facebook_api.api.verify_credentials import verify_user_credentials


urlpatterns = [

    path('credentials/get', GetCredentialAPIView.as_view(), name='get_credentials'),
    path('credentials/post', PostCredentialAPIView.as_view()),
    path('credentials/get-post', ListCreateCredentialAPIView.as_view()),
    path('credentials/<pk>/update', RetrieveUpdateCredentialAPIView.as_view()),
    path('credentials/<pk>/delete', DestroyCredentialAPIView.as_view()),

    # NOTE: Webhook endpoint
    path('webhook/', webhook),

    # NOTE: APIs personalizadas
    path('credentials/verify-credentials', verify_user_credentials, name = 'credentials/verify-credentials')

]