from django.contrib import admin
from applications.facebook_api.models import Credential

# Register your models here.


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'facebook_id', 'access_token')

    search_fields = ['id', 'user', 'facebook_id', 'access_token']


    fieldsets = (
        (None, {
            'fields': ('user', 'facebook_id', 'access_token')
        }),
    )
