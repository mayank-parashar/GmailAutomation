import os

from cryptography.fernet import Fernet

CLIENT_ID = os.environ['client_id']
PROJECT_ID = os.environ['project_id']
AUTH_URI = os.environ['auth_uri']
TOKEN_URI = os.environ['token_uri']
AUTH_PROVIDER_X509_CERT_URL = os.environ['auth_provider_x509_cert_url']
CLIENT_SECRET = os.environ['client_secret']
REDIRECT_URIS = os.environ['redirect_uris']

ENCRYPTION_KEY = os.environ['encryption_key']

cipher_suite = Fernet(ENCRYPTION_KEY)

# DB credentials and other configs can be add here

