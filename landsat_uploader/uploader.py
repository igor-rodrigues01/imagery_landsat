import os

from django.conf import settings
from landsat_extractor.extractor import LandsatExtractor
from imagery.models import Scene, Image, LandsatGrade

from .list_files import ListLandsatImages
from .utils import get_data_from_landsat_image_name
from .KeywordFinder import KeywordFinder


class LandsatUploader():
    """ 
    Class LandsatUploader to extract and create scene and image
    call extract_files to get files extracted and uploaded to models
    Could be initialized with sattelite and quiet variable
    """
    def __init__(self, sat="L8", quiet=True):
        self.sat = sat
        self.path = os.path.join(settings.LANDSAT_IMAGES_PATH, self.sat)
        self.images_list = ListLandsatImages.get_files( path=self.path )
        self.quiet = quiet
<<<<<<< HEAD
        # self.ListLandsatImages = ListLandsatImages()
        # self.images_list = ListLandsatImages.get_files(path=self.path)
    
    def __get_cloud_cover(self, fpath, keyword):
=======

    def __get_cloud_cover(self, fpath, keyword="cloud_cover"):
>>>>>>> f700cc56ad402c5477292ed8093fd35139174af3
        """ Returns cloud cloud_cover with keywordfinder """
        try:
            finder = KeywordFinder(fpath=fpath)
            value = finder.find_keyword(key=keyword)
            value = float(value)
            return value
        except Exception as exc:
            print("\t[ERROR] Metadata with no valid data: {}".format(exc))
            return 0.0
    
    def __get_mtl_file(self, files):
        """ Returns mtl file on files extracted  """
        for file in files:
<<<<<<< HEAD
            if file["type"] == "MTL":
=======
            if file["type"].upper() == "MTL":
>>>>>>> f700cc56ad402c5477292ed8093fd35139174af3
                return file["path"]

        raise ValueError("\t[WARN] Metadata File is not Found")
    
    def __get_scene_name_path(self):
        """ Returns list of files from path with files  """
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
<<<<<<< HEAD
    
=======

    # Change Scene Model
>>>>>>> f700cc56ad402c5477292ed8093fd35139174af3
    def __create_scene(self, image_name, mtl_file=None):
        """
            Create Scene with image_name and metadata file
            using get_data_from_landsat_image_name function from utils and 
            geometry and cloud from self class
            returns scene created
        """
        data    = get_data_from_landsat_image_name(image_name)
        geom    = self.__get_scene_geom(data["path"], data["row"])
        
        if mtl_file is not None:
            cloud   = self.__get_cloud_cover(mtl_file, "CLOUD_COVER")
        else: 
            cloud = 0.0
        
        scene = Scene.objects.get_or_create( # Change Scene Model
            path=data["path"],
            row=data["row"],
            sat="L8",
            date=data["date"],
            name=data["name"],
            cloud_rate=cloud,
            geom=geom,
            status="extracted",
            )

        if not self.quiet:
            print("Scene {} created".format(data["name"]))

        return scene[0]
    
    def __extract_files(self, name, path):
        """
            Extract files using LandsatExtractor
            returns list of images extracted
        """
        extract = LandsatExtractor(name=name, compressed_file=path, quiet=self.quiet)
        return extract.extract_files()

    # Change Image Model
    def __upload_files(self, files, scene):
        """
            Method to create data for Image model with each file from files
            The scene received as arg might be a valid scene to be used as FK
            returns list of images created
        """
        images_created = []

        for file in files:
        
            image = Image.objects.get_or_create( # Change Image Model
                name = file["name"],
                type = file["type"],
                scene = scene,
                path = file["path"]
            )

            if not self.quiet:
                print("Image {} created".format(file["name"]))

            images_created.append(image[0])

        return images_created

    def extract_and_populate_data(self):
        """
            This method extract files using LandsatExtractor module
            and populate data for Image and Scene models.
            returns tuple with scene and images created
        """
        extracted_files = {}

        for file in self.__get_scene_name_path():
             
            files   = self.__extract_files(name=file["name"], path=file["path"])
            fmtl    = self.__get_mtl_file(files)
            scene   = self.__create_scene(file["name"], fmtl)
            images  = self.__upload_files(files, scene)
<<<<<<< HEAD
       
            return (scene, images,)
=======

            extracted_files[ file["name"] ] = {
                "scene": scene,
                "images": images 
                }

        return extracted_files
>>>>>>> f700cc56ad402c5477292ed8093fd35139174af3
