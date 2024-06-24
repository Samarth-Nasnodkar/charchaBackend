from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from Attachment.models import Attachment


# Create your views here.
@csrf_exempt
def fetchAllAttachments(request):
    dbAttachments = Attachment.objects.all()
    return HttpResponse(json.dumps(list(dbAttachments)), content_type="application/json")
