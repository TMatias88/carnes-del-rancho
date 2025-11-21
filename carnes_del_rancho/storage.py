from storages.backends.s3boto3 import S3Boto3Storage

class OverwriteStorage(S3Boto3Storage):
    file_overwrite = True

    def get_available_name(self, name, max_length=None):
        """
        Evita que Django renombre el archivo si existe.
        Si existe, lo borra primero.
        """
        if self.exists(name):
            self.delete(name)
        return name
