import os

# enable CSRF
WTF_CSRF_ENABLED = True
secret_key_generator = os.urandom(24)
# secret key for authentication
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", secret_key_generator)
