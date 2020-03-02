from os import mkdir, path

class SMSProcessor:

    def __init__(self):
        self._outputDir = './output/'   
        if not path.exists(self._outputDir):
            mkdir(self._outputDir)

    def run(self):
        print('Implemented in derived classes')

    