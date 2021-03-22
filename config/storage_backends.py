from storages.backends.s3boto3 import S3Boto3Storage


class S3StaticStorage(S3Boto3Storage):
    location = 'staticfiles'
    default_acl = 'public-read'


class S3MediaStorage(S3Boto3Storage):
    location = 'mediafiles'
    default_acl = 'public-read'
    file_overwrite = False
