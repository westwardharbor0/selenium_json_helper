import datetime
import time
import os

class TestUtils:
    def mfolder(self, path):
        if not os.path.exists(path):
            os.mkdir("{}/".format(path))

    def chmod(self,path):
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)

    def stamp(self, log=None):
        pat = '_%d-%m-%Y_%H_%M_%S'
        if log:
            pat = '%d-%m-%Y %H:%M:%S'
        return str(datetime.datetime.fromtimestamp(
            time.time()).strftime(pat))

    def get_id(self,id):
        return self.driver.find_element_by_id(id)

    def get_class(self,cls):
        return self.driver.find_element_by_class_name(cls)

    def get_selector(self,sel):
        if '#' in sel:
            return self.get_id(sel.replace('#',''))
        return self.get_class(sel.replace('.',''))

    def get_main_folder(self):
        temp =  os.path.realpath(__file__).split('/')
        temp = temp[:-2]
        return '/'.join(temp)
