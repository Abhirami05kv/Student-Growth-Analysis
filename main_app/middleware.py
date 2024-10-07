from django.http import HttpResponse

from main_app.models import Parent


class LoginCheckMiddleWare:
    def __init__(self, get_response):
        return ''