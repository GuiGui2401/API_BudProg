from django.contrib.auth import authenticate
from . import auth_backends
from django.http import JsonResponse

class APIAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION")
        if auth != None:
            string = auth.split()
            if string[0].lower() == "bareer":
                token = string[1]
                try:
                    user = authenticate(auth_token=token)
                except auth_backends.UserError:
                    return JsonResponse({"Error": "Error during authentication."})
                except auth_backends.TokenError:
                    return JsonResponse({"Error": "The token has expired, log in again to gain access to this service"})

                request.user = user
            
        response = self.get_response(request)
        return response