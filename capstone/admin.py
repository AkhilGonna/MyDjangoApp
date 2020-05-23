from django.contrib import admin
from .models import userinfo,language_table,repos_table,job_table,recom_table
# Register your models here.

admin.site.register(userinfo)
admin.site.register(repos_table)
admin.site.register(language_table)
admin.site.register(job_table)
admin.site.register(recom_table)