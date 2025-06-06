import jwt
from jwt import ExpiredSignatureError,InvalidTokenError
from django.conf import settings
from django.http import JsonResponse
from functools import wraps

def token_required(func):
    @wraps(func)
    def wrapper(self,request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Authorization token missing"}, status=401)
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.user_id = decoded_token['user_id']
            request.email = decoded_token['email']
        except ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except jwt.DecodeError:
            return JsonResponse({"error": "Token is invalid"}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper