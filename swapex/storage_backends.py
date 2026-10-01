"""
Custom storage backends for S3
Separates static files from media files in S3 bucket
"""

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Storage backend for static files (CSS, JS, admin files)"""
    location = 'static'
    default_acl = None  # Don't set ACL, let bucket policy handle it
    file_overwrite = False
    querystring_auth = False


class MediaStorage(S3Boto3Storage):
    """Storage backend for media files (user uploads)"""
    location = 'media'
    default_acl = None  # Don't set ACL, let bucket policy handle it
    file_overwrite = False
    querystring_auth = False
