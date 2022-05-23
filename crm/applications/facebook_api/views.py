#!/usr/bin/env python

from django.views.generic import TemplateView, ListView

# Forms
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Models
from django.contrib.auth.models import User


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
