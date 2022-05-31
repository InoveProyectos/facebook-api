#!/usr/bin/env python

from lib2to3.pgen2 import token
from django.views.generic import TemplateView, ListView

# Forms
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Models
from django.contrib.auth.models import User
from applications.facebook_api.models import Credential

from applications.facebook_api.api.verify_credentials import token_is_valid
from applications.facebook_api.classes.FacebookUser import FacebookUser
from applications.facebook_api.classes.FacebookPage import FacebookPage
from applications.facebook_api.classes.Facebook import Facebook

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
        
        else:
            validated = False

        context['validated'] = validated

        return context


class AdminPageView(TemplateView):
    '''
    Página donde el usuario podrá administrar una página
    '''
    template_name = 'facebook_api/admin-page.html'

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(username = self.request.user)
        credential = Credential.objects.filter(user = user.id).first()
        fb_user = FacebookUser(credential.facebook_id, credential.access_token)
        
        page_name = request.POST.get('page_name')
        page_id = request.POST.get('page_id')
        page_access_token = request.POST.get('page_access_token')
        page_picture = request.POST.get('page_picture')

        if not fb_user.is_admin(page_id):
            return HttpResponse(status = 400, content = 'You havent access for managing {page_id}')
            
        page = FacebookPage(page_id, page_access_token, page_name, page_picture)

        context['page'] = page

        return self.render_to_response(context)