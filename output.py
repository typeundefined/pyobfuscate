import os
import shutil
import sys
from tempfile import mkstemp


class BaseWriter(object):
    def write(self, raw_str):
        raise NotImplemented()

    def close(self):
        pass


class StdoutWriter(BaseWriter):
    def write(self, raw_str):
        sys.stdout.write(raw_str)


class FileWriter(BaseWriter):
    def __init__(self, file_name):
        self.target_filename = file_name
        _, self.temp_filename = mkstemp()
        self.file_obj = open(self.temp_filename, 'w')

    def write(self, raw_str):
        self.file_obj.write(raw_str)

    def close(self):
        self.file_obj.close()
        try:
            shutil.copyfile(self.temp_filename, self.target_filename)
        except IOError:
            print >> sys.stderr, 'Failed to write to the file. ' \
                                 'The obfuscated content is left in temporary file %s' % self.temp_filename
            raise
        os.unlink(self.temp_filename)