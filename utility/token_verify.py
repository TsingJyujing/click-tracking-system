from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from config import get_token

def token_required(func):
    """
    Process  automatically
    :param func:
    :return:
    """
    def wrapper(request: HttpRequest) -> HttpResponse:
        try:
            if "token" in request.GET:
                token = request.GET["token"]
            elif "token" in request.POST:
                token = request.POST["token"]
            else:
                raise Exception("Token not found in GET/POST, try to use Django CSRF token.")
            assert token in get_token()
            return func(request)
        except:
            return login_required(func)(request)

    return wrapper
