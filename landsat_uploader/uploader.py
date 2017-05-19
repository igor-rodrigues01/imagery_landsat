import os

from django.conf import settings
from landsat_extractor.extractor import LandsatExtractor

from .models import Scene, Image
from .list_files import ListLandsatImages

class LandsatUploader():
    """ LandsatUploader """
    def __init__(self, sat="L8"):
        self.sat = sat
        self.path = os.path.join(settings.LANDSAT_IMAGES_PATH, self.sat)
        self.images_list = ListLandsatImages( path=self.path )

    def upload_files(self):
        pass