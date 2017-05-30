import os
from django.test import TestCase
from django.conf import settings

from .processor import LandsatColorComposition


def list_paths_to_use():
    return[
        os.path.join(
            settings.MEDIA_ROOT, "L8",
            "LC08_L1TP_231064_20170511_20170511_01_RT",
            "LC08_L1TP_231064_20170511_20170511_01_RT_B6.TIF"),
        os.path.join(
            settings.MEDIA_ROOT, "L8",
            "LC08_L1TP_231064_20170511_20170511_01_RT",
            "LC08_L1TP_231064_20170511_20170511_01_RT_B5.TIF"),
        os.path.join(
            settings.MEDIA_ROOT, "L8",
            "LC08_L1TP_231064_20170511_20170511_01_RT",
            "LC08_L1TP_231064_20170511_20170511_01_RT_B4.TIF"),
    ]


def files_for_composition():
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
            "name": "LC08_L1TP_231064_20170511_20170511_01_RT_B8.TIF",
            "path": os.path.join(
                settings.MEDIA_ROOT, "L8",
                "LC08_L1TP_231064_20170511_20170511_01_RT",
                "LC08_L1TP_231064_20170511_20170511_01_RT_B8.TIF"
            ),
            "type": "B8",
        },
    ]

class TestColorComposition(TestCase):
    print ("--Testing Color Composition")
    def setUp(self):
        self.name = "LC08_L1TP_231064_20170511_20170511_01_RT"
        self.path = os.path.join(settings.MEDIA_ROOT, "L8")
        self.file_list = files_for_composition()
        self.processor = LandsatColorComposition(self.path, self.name, self.file_list)


    def test_set_tiff_file(self):
        self.assertEqual(
            os.path.join(self.path, self.name + "_RGB.tiff"), self.processor._set_full_file_path()
        )

    def test_separate_filelist(self):
        plist = list_paths_to_use()
        self.assertEqual(
            self.processor._separate_filelist(), plist
        )

    def test_create_composition(self):
        final_path = self.processor._set_full_file_path()
        self.assertEqual(
            self.processor.create_composition(), {"name": self.name,
                                                  "path": final_path,
                                                  "type": "RGB"}
        )