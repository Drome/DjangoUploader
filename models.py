from django.db import models
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

import uuid
import os.path

def fileUploadName(instance, filename):
  return "/".join(["uploads",instance.uploadUser,filename])

class UploadToken(models.Model):
  token = models.CharField(max_length=100, unique=True, editable=False, default=uuid.uuid4)
  uploadUser = models.CharField(max_length=100)
  valid = models.BooleanField(default=True)
  reusable = models.BooleanField(default=False)
  uploadedFile = models.FileField(upload_to=fileUploadName, null=True, blank=True, editable=False)
  
  def delete(self, *args, **kwargs):
    self.uploadedFile.delete()
    super(UploadToken, self).delete(*args, **kwargs)
    
  def save(self, *args, **kwargs):
    try:
      old = UploadToken.objects.get(id=self.id)
      print old.uploadedFile.name
      if old.uploadedFile and (old.uploadedFile != self.uploadedFile):
	old.uploadedFile.storage.delete(old.uploadedFile.name)
    except ObjectDoesNotExist:
      pass
    super(UploadToken, self).save(*args, **kwargs)
    
  def file_link(self):
    if self.uploadedFile:
      return "<a href='%s'>%s</a>" % (reverse("uploader-uploads", args=("/".join([self.uploadUser, os.path.basename(self.uploadedFile.name)]),)), format_html(self.uploadedFile.name))
    else:
      return ""
  file_link.allow_tags=True
  
  class Meta:
    permissions = (
      ("can_download", "User is allowed to download uploaded files."),
    )