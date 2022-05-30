from django.contrib import admin
from applications.facebook_api.models import Credential

# Register your models here.


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'expires_in', 'created_at')

    search_fields = ['user', 'access_token', 'expires_in', 'created_at']


    fieldsets = (
        (None, {
            'fields': ('user', 'access_token', 'expires_in', 'created_at')
        }),
    )
