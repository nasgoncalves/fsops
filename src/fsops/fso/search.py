import os

from path import Path

from .file_system_object import Object


class Search(object):

    def __init__(self, path):
        self.path = Path(path)

    def walk(self):
        for root, dirs, files in os.walk(self.path.abspath()):

            for obj in dirs:
                dir_path = Path(root) / obj
                if dir_path.access(os.R_OK):
                    yield Object.from_path(dir_path)

            for obj in files:
                file_path = Path(root) / obj
                if file_path.access(os.R_OK):
                    yield Object.from_path(file_path)
