import requests

from django.core.exceptions import ImproperlyConfigured

from .. import AWS_S3_CUSTOM_DOMAIN, AWS_STORAGE_BUCKET_NAME
from .django import ALLOWED_HOSTS


def _probe_aws_ip():
    try:
        ec2_private_ip = requests.get(
            "http://169.254.169.254/latest/meta-data/local-ipv4", timeout=3
        ).text
    except requests.exceptions.RequestException as e:
        raise ValueError("Could not get EC2 private ip address: {}".format(e))
    else:
        if not ec2_private_ip:
            raise ValueError(
                "Could not get EC2 private ip address: ec2_private_ip={!r}".format(
                    ec2_private_ip
                )
            )
        return ec2_private_ip


ALLOWED_HOSTS.append(_probe_aws_ip())

AWS = True
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "public, max-age=900"}
# #S3 settings
DEFAULT_FILE_STORAGE = "madewithwagtail.s3utils.MediaRootStorage"
STATICFILES_STORAGE = "madewithwagtail.s3utils.StaticRootStorage"

if not AWS_STORAGE_BUCKET_NAME:
    raise ImproperlyConfigured(
        "Wrong AWS_STORAGE_BUCKET_NAME={!r} env variable".format(
            AWS_STORAGE_BUCKET_NAME
        )
    )

if not AWS_S3_CUSTOM_DOMAIN:
    AWS_S3_CUSTOM_DOMAIN = "{}.s3-ap-southeast-2.amazonaws.com".format(
        AWS_STORAGE_BUCKET_NAME
    )

STATIC_URL = "https://%s/static/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN

AWS_S3_FILE_OVERWRITE = False
