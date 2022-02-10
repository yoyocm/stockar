from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from stockar.models import Account, StorageOffer, StorageSpace, AccessCode

admin.site.register(StorageOffer)
admin.site.register(StorageSpace)
admin.site.register(AccessCode)


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'joined_at', 'last_login', 'is_staff', 'is_admin', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'joined_at', 'last_login')
    readonly_fields = ('id', 'joined_at', 'last_login')
    ordering = ('email',)
    add_fieldsets = ((None, {'fields': ('email', 'first_name', 'last_name', 'is_admin', 'is_staff', 'password1', 'password2')}),)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
