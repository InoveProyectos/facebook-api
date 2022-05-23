#!/usr/bin/env python

from django.urls import path
from applications.facebook_api.api.credentials import *


urlpatterns = [

    path('credentials/get', GetCredentialAPIView.as_view(), name='get_credentials'),
    path('comics/post', PostCredentialAPIView.as_view()),
    path('comics/get-post', ListCreateCredentialAPIView.as_view()),
    path('comics/<pk>/update', RetrieveUpdateCredentialAPIView.as_view()),
    path('comics/<pk>/delete', DestroyCredentialAPIView.as_view())

]