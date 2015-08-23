from django.contrib import admin
from django.contrib.auth.models import Group
from accounts.models import Teacher
from accounts.admin_forms import UserChangeForm,UserCreationForm
from django.contrib.auth.admin import UserAdmin

# class PayzaataccountsAdmin(admin.ModelAdmin):

#     list_display = ('balance', )
#     readonly_fields = ('balance', )

#     def __init__(self, *args, **kwargs):
#         super(PayzaataccountsAdmin, self).__init__(*args, **kwargs)
#         self.list_display_links = (None, )

#     def get_actions(self, request):
#         actions = super(PayzaataccountsAdmin, self).get_actions(request)
#         del actions['delete_selected']
#         return actions

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

# admin.site.unregister(Group)
# admin.site.register(Payzataccounts, PayzaataccountsAdmin)
class TeacherAdmin(UserAdmin):
	form = UserChangeForm
  	add_form = UserCreationForm

  	fieldsets = (
        ('Teacher', {
         'fields': ('email', 'first_name','last_name', 'password')}),
        ('User Type', {'fields': ('user_role',)}),
        ('Permissions', {'fields': ('is_active',)})
        
    )

	add_fieldsets = (('Teacher', {'fields': ('first_name','last_name', 'email', 'password1', 'password2', 'user_role', 'is_active')}),)

	list_filter = ()
	list_display = ('first_name', 'last_name', 'email',)

	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(Teacher,TeacherAdmin)
