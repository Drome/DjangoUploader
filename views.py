from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from uploader import forms
from uploader import models

import os.path
import mimetypes

def index(request):
  if not request.method == "POST":
    return render(request, "uploader/index.html", {"form" : forms.UploadForm()})
  form = forms.UploadForm(request.POST, request.FILES)
  if form.is_valid():
    try:
      utoken = models.UploadToken.objects.get(token=form.cleaned_data['token'])
      if not utoken.valid:
	return render(request, "uploader/index.html", {"form" : form, "error" : True, "errorText" : "Invalid token."})
      if utoken.uploadedFile and not utoken.reusable:
	return render(request, "uploader/index.html", {"form" : form, "error" : True, "errorText" : "Reuse of this token was disabled."})
      utoken.uploadedFile = request.FILES['uploadFile']
      utoken.save()
      return redirect('uploader-thanks')
    except ObjectDoesNotExist:
      return render(request, "uploader/index.html", {"form" : form, "error" : True, "errorText" : "Invalid token."})
  else:
    return render(request, "uploader/index.html", {"form" : form})
  
def thanks(request):
  return render(request, "uploader/thanks.html")
  
@user_passes_test(lambda user : user.has_perm('uploader.can_download'))
def uploads(request, upload_id):
  try:
    user, filename = upload_id.split("/")
    utoken = models.UploadToken.objects.get(uploadUser=user, uploadedFile__endswith=filename)
  except:
    raise Http404
  content = utoken.uploadedFile.read() # Only for debugging! Use X-Sendfile instead!
  fname = utoken.uploadedFile.name
  mtype = mimetypes.guess_type(fname)
  mtype = mtype if mtype != "" else "application/octet-stream"
  response = HttpResponse(content, content_type=mtype)
  response['Content-Disposition'] = "attachment; filename="+os.path.basename(fname)
  return response