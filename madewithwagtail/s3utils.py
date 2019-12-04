import mimetypes

from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting

mimetypes.add_type("application/font-woff", "woff", strict=True)
mimetypes.add_type("application/font-woff", "woff2", strict=True)


StaticRootStorage = lambda: S3Boto3Storage(  # noqa: E731
    location=('static/%s' % setting('APPLICATION_VERSION', '')).strip("/"))
MediaRootStorage = lambda: S3Boto3Storage(location="media")  # noqa: E731
