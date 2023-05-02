import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-acwjt8y7mhe56bf8.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    auth_header = request.headers['Authorization']

    if not auth_header:
        raise AuthError("Missing Authorization Header", 401)

    if len(auth_header.split(' ')) != 2:
        raise AuthError("Header is malformed", 401)
    elif auth_header.split(' ')[0].lower() != "bearer":
        raise AuthError("Header is malformed", 401)

    return auth_header.split(' ')[1]


# Check permission
def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError("Token Malformed", 401)

    if permission not in payload["permissions"]:
        raise AuthError("Authentication Error", 403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read)  # get jwt keys
    jwt_header = jwt.get_unverified_header(token)  # get unverified header

    if "kid" not in jwt_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    rsa_key = {}

    for key in jwks:
        if key["kid"] == jwt_header["kid"]:
            rsa_key = {
                "kid": key["kid"],
                "kty": key["kty"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        try:
            payload = jwt.decode(token,
                                 key=rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer=f"https://{AUTH0_DOMAIN}"
                                 )

            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code": "token_expired",
                "description": "Your authorization time has been reached, authorize again."
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                "code": "invalid_claims",
                "description": "Invalid Claims."
            }, 401)
        except Exception:
            raise AuthError({
                "code": "invalid_header",
                "description": "Invalid Header."
            }, 401)

    raise AuthError({
        "code": "invalid_header",
        "description": "Unable to find appropriate key."
    }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
