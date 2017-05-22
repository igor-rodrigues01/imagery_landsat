import os
import shutil


from django.test import TestCase
from django.conf import settings

from .extractor import LandsatExtractor


def create_list():
    image_list = [] 

    for i in range(1,12):
        img = "LC08_L1TP_231064_20170511_20170511_01_RT_B{}.TIF".format(i)
        image_list.append(img)

    # image_list.append("LC08_L1TP_231064_20170511_20170511_01_RT_BQA.TIF")
    # image_list.append("LC08_L1TP_231064_20170511_20170511_01_RT_ANG.txt")
    image_list.append("LC08_L1TP_231064_20170511_20170511_01_RT_MTL.txt")

    return image_list

def files_to_extract():
    return [
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B4.TIF", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_B4.TIF"
                ),
            "type": "B4",            
        },
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B5.TIF", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_B5.TIF"
                ),
            "type": "B5",
        },
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B6.TIF", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_B6.TIF"
                ),
            "type": "B6",
        },
        {
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_MTL.txt", 
            "path": os.path.join( 
                settings.MEDIA_ROOT, "L8", 
                "LC08_L1TP_231064_20170511_20170511_01_RT", 
                "LC08_L1TP_231064_20170511_20170511_01_RT_MTL.txt"
                ),
            "type": "MTL",
        },
    ]

class TestExtraction(TestCase):

    def setUp(self):
        self.name = "LC08_L1TP_231064_20170511_20170511_01_RT"
        file = "{}.tar.gz".format(self.name)

        self.file = os.path.join(settings.LANDSAT_IMAGES_PATH, "L8", file)
        self.files_extracted = []
        self.image_list = create_list()
        self.extractor = LandsatExtractor(self.name, self.file, quiet=False)

    def test_tarfile_isvalid(self):
        self.assertTrue( self.extractor._test_tarfile() )

    def test_interest_bands(self):
        bands = self.extractor._interest_bands(bands=range(1,12))
        for i in bands:
            self.assertTrue(i in self.image_list)

    def test_extraction_files(self):
        self.files_extracted = self.extractor.extract_files()
        
        self.assertEqual(
            self.files_extracted, files_to_extract()
        )

    def tearDown(self):
        path = os.path.join(settings.LANDSAT_IMAGES_PATH, "L8", self.name)
        if os.path.isdir( path ):
            shutil.rmtree( path )