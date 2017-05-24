import  tarfile
import string

class KeywordFinder():

    def __init__(self, fpath, keyword=None):
        self.file_path = fpath
        self.keyword = keyword

        if self.keyword is not None:
            self.find_keyword(keyword)


    def __decode_utf8(self, content):
        new_content = []
        for c in content:
            new_content.append(c.decode('utf-8'))
        return new_content


    def __open_file(self):
        try:
            if (self.file_path.endswith('.tar.gz')):
                tar = tarfile.open(self.file_path)
                for member in tar.getmembers():
                    fp = tar.extractfile(member)
                    if fp:
                        byte_content = fp.readlines()
                        content = self.__decode_utf8(byte_content)
                        return content
            else:
                with open(self.file_path, "r") as fp:
                    content = fp.readlines()
                    return content

        except IOError as e:
            print ("I/O error({0}): {1}.".format(e.errno, e.strerror))
        
        except:
            pass


    # Assuming that on the first occurrence, it returns its value
    def find_keyword(self, key=None):
        fp_content = self.__open_file()

        try:
            if key is not None:
                self.keyword = key
            elif self.keyword is None and key is None:
                raise ValueError('Error: Keyword is empty.')
            
            for line in fp_content:
                line_split = line.lower().split()           
                if self.keyword.lower() in line_split:
                    return self.__return_values(line)

            raise ValueError('Error: Keyword is empty.')

        except ValueError as e:
            print(e)

        except: 
            print ("Error: Unexpected error.")

    def __return_values(self,line):
        t = tuple(line.strip().split(' = '))
        return t[1]
