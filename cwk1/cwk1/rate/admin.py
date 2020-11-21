from django.contrib import admin

# Register your models here.
from .models import Professor, Module, ModuleState, ProfessorRating

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code','name']

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['name','code']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['professor','rating','user']


class ModuleSateAdmin(admin.ModelAdmin):
    list_display = ['module', 'semester', 'year']


admin.site.register(Professor,ProfessorAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(ModuleState, ModuleSateAdmin)
admin.site.register(ProfessorRating, RatingAdmin)