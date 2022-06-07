from django.contrib import admin
from applications.facebook_api.models import Credential, Page, Response


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
    list_display = ('id', 'page_id', 'access_token', 'owner', 'name', 'url', 'picture')

    search_fields = ['id', 'page_id', 'access_token', 'owner', 'name', 'url', 'picture']

    fieldsets = (
        (None, {
            'fields': ('page_id', 'access_token', 'owner', 'name', 'url', 'picture')
        }),
    )

@admin.register(Response)
class RespondeAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'tag', 'message')
    
    search_fields = ['id', 'page', 'tag', 'message']

    fieldsets = (
        (None, {
            'fields': ('page', 'tag', 'message')
        }),
    )