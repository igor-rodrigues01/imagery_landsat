import os
import shutil
from django.test import TestCase
from django.conf import settings
from .processor import LandsatColorComposition
from landsat_extractor.extractor import LandsatExtractor


def files_for_composition(file_list):
    """ Return the testing list in required order """
    test_oredered_list = [{}, {}, {}]
    for file in file_list:
        if file["type"] == "B6":
            test_oredered_list[0] = file["path"]
        elif file["type"] == "B5":
            test_oredered_list[1] = file["path"]
        elif file["type"] == "B4":
            test_oredered_list[2] = file["path"]


    return test_oredered_list

class TestColorComposition(TestCase):
    print ("--Testing Color Composition")

    def setUp(self):
        self.name = "LC08_L1TP_231064_20170511_20170511_01_RT"
        self.path = os.path.join(settings.MEDIA_ROOT, "L8", self.name)
        file = "{}.tar.gz".format(self.name)
        self.file = os.path.join(settings.LANDSAT_IMAGES_PATH, "L8", file)
        self.file_list = {}
        self.extractor = LandsatExtractor(name=self.name,
                                          compressed_file=self.file, quiet=True)

    def test_create_composition(self):
        ## extract files to test rgb composition
        ext_files = self.extractor.extract_files()
        self.file_list = files_for_composition(ext_files) # put them in the needed order
        processor = LandsatColorComposition(self.path, self.name, self.file_list)

        """ Test creation of final file path for composition"""
        self.assertEqual(
            os.path.join(self.path, self.name + "_RGB.TIF"),
            processor._set_full_file_path()
        )

        """ Test creation of colored composition """
        final_path = processor._set_full_file_path()
        self.assertEqual(
            processor.create_composition(), {"name": self.name,
                                                  "path": final_path,
                                                  "type": "RGB"}
        )

    def tearDown(self):
        rm_path = os.path.join( settings.MEDIA_ROOT, "L8", self.name )
        if os.path.exists( rm_path ): # Delete created files in tests in MEDIA_ROOT
            shutil.rmtree( rm_path )