import os
import subprocess

class LandsatColorComposition():
    """ 
    Class that process and create colored composition from Landsat list of files.
    Receive path to save resulting file, file name and ordered file list to 
    create composition.
        
    """
    def __init__(self, out_path, name, file_list, quiet=True):
        self.out_path   = out_path
        self.name       = name
        self.file_list  = file_list     # ordered file list to merge
        self.quiet      = quiet

    def _set_full_file_path(self):
        """
        Returns complete file path for rgb composition 
        """
        if self.name.endswith(".TIF"):
            file_path = os.path.join(self.out_path, self.name)
        else:
            file_path = os.path.join(self.out_path, self.name + "_RGB.TIF")

        return (file_path)

    def create_composition(self):
        """ Creates rgb composition using gdal_merge.py """
        file_path = self._set_full_file_path()

        if not self.quiet:
            print("-- Creating file composition to {}".format(file_path))
            quiet = ""
        else: 
            quiet = "-q"

        gdal_mergepy_command = "gdal_merge.py {} -separate -co \
                                PHOTOMETRIC=RGB -o {}".format(quiet, file_path)

        for file in self.file_list:
            gdal_mergepy_command += " " + file["path"]

        subprocess.call(gdal_mergepy_command, shell=True)

        if os.path.isfile(file_path):
            return {"name": self.name, "path": file_path, "type": "RGB"}
        else:
            return None