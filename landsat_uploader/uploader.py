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
        self.images_list = ListLandsatImages.get_files( path=self.path )

    def _upload_files(self):
        pass    

    def _extract_file(self, name, path):
        extract = LandsatExtractor(name=name, path=path)
        return extract.extract_files()

    def _get_image_name_path(self):
        return [{
            "name": file.split('.')[0], # Change to Regex 
            "path": os.path.join( self.path, file )
        } for file in self.images_list ]

    def extract_files(self):
        pass







