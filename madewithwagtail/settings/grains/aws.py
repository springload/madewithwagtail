import os


import requests

from django.core.exceptions import ImproperlyConfigured

from .. import AWS_S3_CUSTOM_DOMAIN, AWS_STORAGE_BUCKET_NAME
from .django import ALLOWED_HOSTS

def _probe_aws_ip():
    # Determine the runtime environment
    if os.environ.get("ECS_CONTAINER_METADATA_URI_V4"):
        # If running on Fargate with platform version 1.4.0 or later
        metadata_uri = os.environ["ECS_CONTAINER_METADATA_URI_V4"]
        try:
            response = requests.get(f"{metadata_uri}/task", timeout=3)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            # Assume the first network interface's private IP is what we need
            ec2_private_ip = data["Containers"][0]["Networks"][0]["IPv4Addresses"][0]
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not get Fargate task's private IP address: {e}")
    else:
        # Assume running on EC2 or similar environment with access to the traditional metadata service
        try:
            ec2_private_ip = requests.get(
                "http://169.254.169.254/latest/meta-data/local-ipv4", timeout=3
            ).text
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not get EC2 private ip address: {e}")

    if not ec2_private_ip:
        raise ValueError(
            f"Could not get private ip address: ec2_private_ip={ec2_private_ip!r}"
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
