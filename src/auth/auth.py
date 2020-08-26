import json, os
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Read environment variables for use.
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'fsnd-capstone-silo.au.auth0.com')
ALGORITHMS = os.environ.get('ALGORITHMS', ['RS256'])
API_AUDIENCE = os.environ.get('API_AUDIENCE', 'casting_agency_api')

'''
Error handling
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
Gets the token from Authorization header.
Returns the token.
'''
def get_token_auth_header():
    # Get the Authorization header from the request.
    auth = request.headers.get('Authorization', None)

    # Check if header is present, otherwise throw error.
    if auth is None:
        raise AuthError({
            'code': 'missing_authorization_header',
            'description': 'Authorization header is expected.'
        }, 401)

    # Parse the value to get the actual token
    header_parts = auth.split()

    # Validate the header value.
    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(header_parts) < 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(header_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    
    # Get the token from the parsed header.
    token = header_parts[1]
    return token

'''
Decode the given JWT token and verify that its using Auth0 /.well-known/jwks.json
Returns the decoded payload.
'''
def verify_decode_jwt(token):
    # Load the public keys from our AUTH0_DOMAIN to verify the given token.
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get decoded value of the token to check KeyIDs.
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # Find the matching RSA key from the public key matching the given token.
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Use the rsa_key to decode the token, handle errors and return payload.
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
                'description': 'Incorrect claims.\
                     Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 401)

'''
Checks that given permissions are available in the payload.
Returns True if permissions match otherwise raises AuthError.
'''
def check_permissions(permission, payload):
    # Check that permissions are included in the payload.
    if payload['permissions'] is None:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must include permissions.'
        }, 401)
    # Check that requested permission is in the payload.
    # 403 error code is appropriate for authorization errors.
    elif permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized_request',
            'description': 'No permission to perform the request.'
        }, 403)

    return True

'''
@requires_auth(permission) decorator method checks the user permissions.
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get token from header
            token = get_token_auth_header()
            # decode JWT and get payload
            payload = verify_decode_jwt(token)
            # check if user has permissions
            has_permission = check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator