
from .utils import TestUtils
import os

class TestLogger(TestUtils):

    def console_log(self, msg):
        self.write_file("console", msg);

    def error_log(self, msg):
        self.write_file("error", msg, over=True);

    def progress_log(self, msg):
        self.write_file("progress", msg);

    def write_file(self, file, msg, over=False):
        file = self.folder+"/"+self.test_name+"/"+file+".log"
        if not os.path.exists(file) or over:
            open(file, 'w+')
        log = open(file,'a')
        state = self.stamp(log=True)+" | "+file+" | "+msg
        print(msg)
        log.write(state+"\n")
        log.close()
