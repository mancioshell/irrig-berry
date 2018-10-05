
import os
import json
from waterberry.utils.definition import ROOT_DIR

class FileReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def readFile(self):
        file = os.path.join(ROOT_DIR, self.filepath)
        with open(file) as f:
            data = json.load(f)
            return data