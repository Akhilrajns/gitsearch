from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from user.models import GithubUser, ApiSearchDetail
from django.utils.safestring import mark_safe
# Register your models here.

class GitUserAdmin(UserAdmin, admin.ModelAdmin):
    add_form = UserCreationForm
    list_display = ('id', 'login',)
    list_filter = ('created_date',)

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'company', 'location')}),
        (_('Datas'), {'fields': ('gists_url', 'received_events_url', 'url', 'type', 'score', 'avatar_image',
                                 'events_url', 'gravatar_id', 'organizations_url', 'starred_url', 'html_url',
                                 'subscriptions_url', 'site_admin', 'repos_url'

                                 )}),
        (_('Important dates'), {'fields': ('created_date', 'modified_date', )})
    )

    search_fields = ('login', 'email', 'name')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', )
        }),
    )
    ordering = ('login', )
    readonly_fields = ('created_date', 'modified_date', 'avatar_image')
    list_per_page = 10
    ordering = ['-id', ]

    def avatar_image(self, instance):
        return mark_safe(
            '<img src="%s"/ width="100" height="100">' % str(instance.avatar_url)
        )


class ApiSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'query_params')

admin.site.register(GithubUser, GitUserAdmin)
admin.site.register(ApiSearchDetail, ApiSearchAdmin)
