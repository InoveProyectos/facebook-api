#!/usr/bin/env python

from django.views.generic import TemplateView, ListView

# Forms
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Models
from django.contrib.auth.models import User
from applications.facebook_api.models import Credential, Page

from applications.facebook_api.classes.FacebookUser import FacebookUser
from applications.facebook_api.classes.FacebookPage import FacebookPage
from applications.facebook_api.tools.credentials_tools import token_is_valid

from django.http import HttpResponse

# NOTE: Registro e inicio de sesión

class BaseView(TemplateView):
    '''
    Base template
    '''
    template_name = 'facebook_api/base.html'


class LoginUserView(TemplateView):
    '''
    Formulario de inicio de sesión.
    '''
    template_name = 'facebook_api/login.html'


class UserForm(UserCreationForm):
    '''
    Formulario de creación de usuario.
    '''

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')


def register(request):
    '''
    Registro de usuario.
    
    Redireccionamientos:
        - información inválida: /signup
        - registro exitoso: /login
    '''

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            # Guardar el formulario si este es válido
            form.save()
            
            # Redirigin a página de inicio de sesión
            return redirect('/facebook/login')

    else:

        # Crear un objeto de tipo formulario y enviarlo al contexto de renderización
        form = UserForm()
    
    return render(request, 'facebook_api/signup.html', dict(form = form))


class IndexView(TemplateView):
    '''
    Página principal del sitio.
    '''

    template_name = 'facebook_api/index.html'


class DashboardView(TemplateView):
    '''
    Página donde el usuario podrá interactuar con su Facebook
    '''
    
    template_name = 'facebook_api/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(username = self.request.user)
        credential = Credential.objects.filter(user = user.id).first()

        # Si el usuario no tiene credenciales, no validar sección para ver sus páginas (tecnicamente, imposible)
        if not credential:
            validated = False    
            return context    

        fb_user = FacebookUser(credential.facebook_id, credential.access_token)
        pages = fb_user.get_owned_pages()
        context['pages'] = pages

        # Si el usuario no tiene páginas, no validar sección para ver páginas    
        if pages:
            validated = True

            # Registrar páginas en la base de datos
            for page in pages:

                page_obj = Page.objects.filter(page_id = page.id).first()

                if not page_obj:
                    # Si la página no existe, crearla
                    page_obj = Page(owner=credential, page_id=page.id, page_access_token=page.access_token,
                                    name=page.name, url=page.url, picture=page.picture)

                    page_obj.save()
                
                else: 
                    # Si la página existe, actualizar valores sujetos a cambio
                    page_obj.access_token = page.access_token
                    page_obj.name = page.name
                    page_obj.picture = page.picture

                    page_obj.save()

        else:
            # validated = False
            # harcodeado
            validated = True

        context['validated'] = validated

        return context


class AdminPageView(TemplateView):
    '''
    Página donde el usuario podrá administrar una página
    '''
    template_name = 'facebook_api/admin-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_id = kwargs['id']

        user = User.objects.get(username = self.request.user)
        credential = Credential.objects.get(user = user.id)
        page = Page.objects.get(page_id = page_id)

        fb_user = FacebookUser(credential.facebook_id, credential.access_token)

        if not fb_user.is_admin(page.page_id):
            # Acá sería bueno hacer un blueprint en dashboard informando que intentaste acceder al administrador de una página que no tenés permiso
            return redirect('/facebook/dashboard')
        
        context['page'] = page

        return context
