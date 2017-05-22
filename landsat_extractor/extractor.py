import os
import tarfile
from django.conf import settings


class LandsatExtractor():
    """ Class that validate and extract images from Landsat zipFile """

    def __init__(self, name, compressed_file, sat="L8", bands=[4,5,6], quiet=False):
        # super(LandsatUtil, self).__init__()
        self.name               = name
        self.compressed_file    = compressed_file
        self.sattelite          = sat
        self.bands              = bands
        self.quiet              = quiet

    def media_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.sattelite, self.name)

    def _interest_bands(self, bands=None):
        if bands is not None:
            i_bands = bands
        else:
            i_bands = self.bands

        bands = ["{}_B{}.TIF".format(self.name, band_num) for band_num in i_bands]
        bands.append( "{}_MTL.txt".format( self.name ) )

        return bands

    def _test_tarfile(self):
        if not self.quiet:
            print("-- Testing if tarfile is a valid tarfile")
        
        return tarfile.is_tarfile(self.compressed_file)

    def _open_tar_file(self):
        if self._test_tarfile():
            try:
                if not self.quiet:
                    print("-- Opening {}".format(self.compressed_file))

                tar = tarfile.open(self.compressed_file)
                return tar
            except Exception as exc:
                raise ValueError("Bad TarFile with exception: {}".format(exc))

        return False


    def _list_files(self, tar):
        return [image.name for image in tar]

    def _validate_file_extracted(self, i_file, o_path):
        if i_file in os.listdir(o_path):
            if not self.quiet:
                print("\t- File {} - OK".format(i_file))
            return True

    def _extract_interest_bands(self, tar, path=None):
        if path is not None:
            path = path
        else:
            path = self.media_path()

        images = self._list_files(tar)

        extracted_files = []
        for img in self._interest_bands():
            
            if img in images:
                
                if not self.quiet:
                    print("-- Extracting {} to path {}...".format(img, path))

                tar.extract(img, path)

                if self._validate_file_extracted( img, path ):
                    extracted_files.append({
                        "name": img, 
                        "path": os.path.join( path, img ), 
                        "type": img.split(".")[0].split("_")[-1]
                        })
                else: 
                    raise ValueError("[ERROR] File not extracted {}".format(img))

        return extracted_files

    def extract_files(self):
        tar = self._open_tar_file()

        if tar:
            extracted_files = self._extract_interest_bands(tar)
            return extracted_files

        return False
