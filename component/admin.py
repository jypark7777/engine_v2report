from django.contrib import admin
from django.apps import apps
from component.models.account import Tag

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['code', 'name', 'category']
    list_filter = ['category']

    list_per_page = 20

admin.site.register(Tag, TagAdmin)

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)

class ListModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListModelAdmin, self).__init__(model, admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        if 'django.' not in str(model) and __package__ in str(model):
            admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
