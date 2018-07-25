from django.contrib import admin

from apps.tech import models

admin.register(models.RawDataTask)
admin.register(models.RawDataTaskForm)
admin.register(models.RcModify)
admin.register(models.RcModifyForm)

admin.site.register(models.RcModify)
admin.site.register(models.RawDataTask)


