import os

from django.conf import settings
from landsat_extractor.extractor import LandsatExtractor

from .models import Scene, Image, LandsatGrade
from .list_files import ListLandsatImages
from .utils import get_data_from_landsat_image_name
from .KeywordFinder import KeywordFinder

class LandsatUploader():
    """ LandsatUploader """
    def __init__(self, sat="L8", quiet=True):
        self.sat = sat
        self.path = os.path.join(settings.LANDSAT_IMAGES_PATH, self.sat)
        self.images_list = ListLandsatImages.get_files( path=self.path )
        self.quiet = quiet

    def __get_cloud_cover(self, fpath, keyword):
        try:
            finder = KeywordFinder(fpath=fpath)
            value = finder.find_keyword(key=keyword)
            value = float(value)
            return value
        except Exception as exc:
            print("\t[ERROR] Metadata with no valid data: {}".format(exc))
            return 0.0

    def __get_mtl_file(self, files):
        for file in files:
            if file["type"].upper == "MTL":
                return file["path"]

        raise ValueError("\t[WARN] Metadata File is not Found")

    def __get_scene_name_path(self):
        return [{
            "name": file.split('.')[0], # Change to Regex 
            "path": os.path.join( self.path, file )
        } for file in self.images_list ]
    
    def __get_scene_geom(self, path, row):
        """ Returns geometry from LandsatGrade model """
        try:
            path_row = LandsatGrade.objects.get(path=int(path), row=int(row))
            return path_row.geom
        except Exception as exc:
            print("\t[ERROR] Path and Row is not valid!")

        return False


    def _create_scene(self, image_name, mtl_file=None):
        data    = get_data_from_landsat_image_name(image_name)
        geom    = self.__get_scene_geom(data["path"], data["row"])
        
        if mtl_file is not None:
            cloud   = self.__get_cloud_cover(mtl_file, "CLOUD_COVER")
        else: 
            cloud = 0.0
        
        scene = Scene.objects.get_or_create(
            path=data["path"],
            row=data["row"],
            sat="L8",
            date=data["date"],
            name=data["name"],
            cloud_rate=cloud,
            geom=geom,
            status="downloaded",
            )

        if not self.quiet:
            print("Scene {} created".format(data["name"]))

        return scene[0]

    def _extract_files(self, name, path):
        extract = LandsatExtractor(name=name, compressed_file=path)
        return extract.extract_files()

    def _upload_files(self, files, scene):
        images_created = []

        for file in files:
        
            image = Image.objects.get_or_create(
                name = file["name"],
                type = file["type"],
                scene = scene,
                path = file["path"]
            )

            if not self.quiet:
                print("Image {} created".format(file["name"]))

            images_created.append(image)

        return images_created

    def extract_files(self):

        for file in self.__get_scene_name_path():
            files   = self._extract_files(name=file["name"], path=file["path"])
            fmtl    = self.__get_mtl_file(files)
            scene   = self._create_scene(self, file["name"], mtl)

            self._upload_files(files, scene)
