from django.contrib import admin

from apps.blog import models

admin.site.register(models.User)
admin.site.register(models.WeekReport)
admin.site.register(models.ProjectUser)
admin.site.register(models.ProjectName)
admin.site.register(models.Project)
admin.site.register(models.ProjectType)

