from storages.backends.s3boto3 import S3Boto3Storage

class OverwriteStorage(S3Boto3Storage):
    """
    Storage que sobrescribe archivos existentes en DigitalOcean Spaces.
    No permite que Django genere nombres con hash (_ASD123.png).
    """
    file_overwrite = True

    def get_available_name(self, name, max_length=None):
        # Si el archivo existe en Spaces, se borra primero
        if self.exists(name):
            self.delete(name)
        return name
