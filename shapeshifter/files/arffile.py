import os
import tempfile

from ..utils import arff_to_pandas, to_arff
from ..files import SSFile


class ARFFFile(SSFile):

    def read_input_to_pandas(self, columnList=[], indexCol="Sample"):
        if self.isGzipped:
            tempFile = super()._gunzip_to_temp_file()
            df= arff_to_pandas(tempFile.name)
            os.remove(tempFile.name)
        else:
            df = arff_to_pandas(self.filePath)
        if len(columnList) > 0:
            df = df[columnList]
        return df


    def write_to_file(self, df, gzipResults=False, includeIndex=False, null='NA', indexCol="Sample", transpose=False):
        if gzipResults:
            tempFile = tempfile.NamedTemporaryFile(delete=False)
            to_arff(df, tempFile.name)
            tempFile.close()
            super()._gzip_results(tempFile.name, self.filePath)
        else:
            to_arff(df, super()._remove_gz(self.filePath))





