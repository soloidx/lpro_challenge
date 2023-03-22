from .base import *

ALLOWED_HOSTS = ["zmm1wgh21d.execute-api.us-east-1.amazonaws.com"]

INSTALLED_APPS += ["storages"]

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL="public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

