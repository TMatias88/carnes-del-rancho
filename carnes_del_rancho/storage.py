from storages.backends.s3boto3 import S3Boto3Storage

class StaticNameStorage(S3Boto3Storage):
    file_overwrite = True
    def get_available_name(self, name, max_length=None):
        # NO permite agregar sufijos, usa el nombre tal cual
        return name
