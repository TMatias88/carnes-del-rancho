from storages.backends.s3boto3 import S3Boto3Storage

class StaticNameStorage(S3Boto3Storage):
    file_overwrite = True          # NO crear nombres raros
    custom_domain = False          # Evita confusiones con el endpoint
