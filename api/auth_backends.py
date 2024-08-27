from django.contrib.auth.models import User
from jose import jwt
import datetime

class AuthenticationError(Exception):
    """ Custum exception for authentication errors """
    pass

class UserError(AuthenticationError):
    pass

class TokenError(AuthenticationError):
    """ Custom exception for token expiration error """
    pass

class APIAuthBackend:
    """
        Custom backend for api authentication
    """

    def authenticate(self, request, auth_token=None):
        if auth_token == None:
            return None
        
        return self.authenticate_credentials(auth_token)

    def authenticate_credentials(self, payload):
        decoded = jwt.decode(payload, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms=['HS256'])
        username = decoded.get('user', None)
        expiry = decoded.get('expiry', None).split('/') #we split content of expiry string dd/mm/yyyy
        expiry = datetime.date(day=int(expiry[0]), month=int(expiry[1]), year=int(expiry[2]))

        user = None

        try:
            user = objects.get(username=username)
        except:
            raise UserError("This user does not exist")

        if not user.is_active:
            raise UserError("This user is not active or deleted")

        if expiry < datetime.date.today():
            raise TokenError("Token has expired")

        return user