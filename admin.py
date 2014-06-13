from django.contrib import admin
from uploader.models import UploadToken

class UploadTokenAdmin(admin.ModelAdmin):
  list_display = ['uploadUser', 'token', 'valid', 'reusable', 'uploadedFile', 'file_link']

admin.site.register(UploadToken, UploadTokenAdmin)