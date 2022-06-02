from django.contrib import admin
from applications.facebook_api.models import Credential, Page


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'facebook_id', 'access_token')

    search_fields = ['id', 'user', 'facebook_id', 'access_token']


    fieldsets = (
        (None, {
            'fields': ('user', 'facebook_id', 'access_token')
        }),
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'page_id', 'page_access_token', 'owner', 'name', 'url', 'picture')

    search_fields = ['id', 'page_id', 'page_access_token', 'owner', 'name', 'url', 'picture']

    fieldsets = (
        (None, {
            'fields': ('page_id', 'page_access_token', 'owner', 'name', 'url', 'picture')
        }),
    )