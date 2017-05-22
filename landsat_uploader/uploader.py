import os

from django.conf import settings
from landsat_extractor.extractor import LandsatExtractor

from .models import Scene, Image
from .list_files import ListLandsatImages
from .utils import get_data_from_landsat_image_name

class LandsatUploader():
    """ LandsatUploader """
    def __init__(self, sat="L8"):
        self.sat = sat
        self.path = os.path.join(settings.LANDSAT_IMAGES_PATH, self.sat)
        self.images_list = ListLandsatImages.get_files( path=self.path )

    def _get_scene_name_path(self):
        return [{
            "name": file.split('.')[0], # Change to Regex 
            "path": os.path.join( self.path, file )
        } for file in self.images_list ]
    
    def _create_scene(self, image_name):
        data = get_data_from_landsat_image_name(image_name)

        scene = Scene.objects.get_or_create(
            path=data["path"],
            row=data["row"],
            sat="L8",
            date=data["date"],
            name=data["name"],
            cloud_rate=0.0,
            geom="POLYGON((-71.1776585052917 42.3902909739571,-71.1776820268866 42.3903701743239,-71.1776063012595 42.3903825660754,-71.1775826583081 42.3903033653531,-71.1776585052917 42.3902909739571))",
            status="downloaded",
            )

        return scene[0]

    def _extract_file(self, name, path):
        extract = LandsatExtractor(name=name, compressed_file=path)
        return extract.extract_files()

    def _upload_files(self, files, scene):
        for file in files:
            Image.objects.get_or_create(
                name = file["name"],
                type = file["type"],
                scene = scene,
            )
        pass

    def extract_files(self):

        for file in self._get_scene_name_path():

            scene = self._create_scene(self, file["name"])
            files = self._extract_file(name=file["name"], path=file["path"])

            self._upload_files(files, scene)
