from django.contrib import admin

from departament.models import Departament


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    pass
