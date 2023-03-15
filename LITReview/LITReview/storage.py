from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CustomStorage(FileSystemStorage):
    def __init__(self, location=None):
        if location is None:
            location = settings.MEDIA_ROOT
        super().__init__(location)

    def get_available_name(self, name, max_length=None):
        # Remove spaces from the filename.
        name = name.replace(' ', '_')
        return super().get_available_name(name, max_length)
