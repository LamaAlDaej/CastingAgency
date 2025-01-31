import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN=os.environ.get('AUTH0_DOMAIN')
ALGORITHMS=os.environ.get('ALGORITHMS')
API_AUDIENCE=os.environ.get('API_AUDIENCE')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    """
    Reference: 
    - Identity and Access Management course's videos
    - https://github.com/udacity/FSND/tree/master/BasicFlaskAuth
    """
    # Check if the Authorization header exists
    if 'Authorization' not in request.headers:
        # if not, raise an AuthError (no header is present)
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # Get the Authorization header and store it in a variable
    auth_header = request.headers['Authorization']
    # Split the Authorization header and store them in a variable
    header_parts = auth_header.split(' ')

    # Check if the Authorization header starts with Bearer
    if header_parts[0].lower() != 'bearer':
        # if not, raise an AuthError (the header is malformed)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    # Check if the token exists
    elif len(header_parts) == 1:
        # if not, raise an AuthError (the header is malformed)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    # Check if the Authorization header is Bearer token
    elif len(header_parts) > 2:
        # if not, raise an AuthError (the header is malformed)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    # Return the token part of the header
    return header_parts[1]

def check_permissions(permission, payload):
    """
    Reference:
    - Identity and Access Management course's videos
    - https://github.com/udacity/FSND/tree/master/BasicFlaskAuth
    """
    # Check if the permissions included in the payload
    if 'permissions' not in payload:
        # if not, raise an AuthError (permissions are not included in the payload)
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    # Check if the requested permission string is in the payload permissions array
    if permission not in payload['permissions']:
        # if not, raise an AuthError (the requested permission string is not in the payload permissions array)
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    # return True
    return True

def verify_decode_jwt(token):
    """
    Reference:
    - Identity and Access Management course's videos
    - https://github.com/udacity/FSND/tree/master/BasicFlaskAuth
    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

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
