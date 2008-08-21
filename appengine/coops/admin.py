from django.contrib import admin
from coops.models import Coop, Organization

class CoopAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'record_modified', 'record_added')
    date_hierarchy = 'record_modified'
    fieldsets = (
            (None, {
                'fields': ('name', 'street_address_1', 'street_address_2', 'city', 'state', 'zip_code', 'phone', 'public_email'),
            }),
            (None, {
                'fields': ('number_of_residents', 'average_rent', 'founded', 'description', 'picture', 'organization')
            }),
                
    )
    def allow_contact_or_superuser(self, request, obj, super_can):
        if request.user.is_superuser or not obj:
            return super_can
        return not(not obj.contacts.filter(id__exact = request.user.id))

    # permission to change only if superuser or a contact for the coop
    def has_change_permission(self, request, obj=None):
        return self.allow_contact_or_superuser(request, obj,
                super(CoopAdmin, self).has_change_permission(request, obj))

    # permission to delete only if superuser or a contact for the coop
    def has_delete_permission(self, request, obj = None):
        return self.allow_contact_or_superuser(request, obj,
                super(CoopAdmin, self).has_delete_permission(request, obj))

    # superuser sees all; regular user sees only their own
    def queryset(self, request):
        qs = super(CoopAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(contacts__id__exact = request.user.id)

admin.site.register(Coop, CoopAdmin)
admin.site.register(Organization)
