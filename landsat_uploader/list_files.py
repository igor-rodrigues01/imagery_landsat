import os
from django.conf import settings


class ListLandsatImages:
    """Class to return Landast List images from path"""
    def get_files(path=None, sat="L8", ext="tar.gz"):

        if path is not None:
            path = path
        else:
            path = os.path.join(settings.LANDSAT_IMAGES_PATH, sat)

        return [ file for file in os.listdir(path) if file.endswith(ext) ]
