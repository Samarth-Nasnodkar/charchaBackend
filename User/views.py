import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .controller.UserController import UserController


# Create your views here.
@csrf_exempt
def fetchUser(request):
    email = request.GET.get('email')
    userController = UserController(email)
    if not userController.userExists:
        return HttpResponse('Not user exists with email <{}>'.format(email))

    return HttpResponse(userController.serialize(userController.user), content_type='application/json')


@csrf_exempt
def fetchAllUsers(request):
    allUsers = UserController.fetchAllUsers()
    return HttpResponse(allUsers, content_type='application/json')


@csrf_exempt
def updateUser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    email = body.get('email', '')
    update = body.get('update', None)

    if update is None:
        return HttpResponse('No update data')

    userController = UserController(email)
    if not userController.userExists:
        return HttpResponse('Not user exists with email <{}>'.format(email))

    res = userController.updateUser(update)
    if not res:
        return HttpResponse('Update failed')

    return HttpResponse(UserController.serialize(userController.user), content_type='application/json')
