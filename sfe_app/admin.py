from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from sfe_app.models import *


# Register your models here.


class CustomUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


admin.site.register(CustomUser, CustomUserAdmin)


class SupportModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


admin.site.register(SupportModel, SupportModelAdmin)


class AddVideoModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


admin.site.register(AddVideoModel, AddVideoModelAdmin)
