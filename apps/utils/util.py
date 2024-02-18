import datetime
import os

import pandas as pd
from logger_util import UtxLogger as log


class UtxUtils:

    def __init__(self):
        self.log = log(self.__class__.__name__)

    def export_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        file_exists = os.path.isfile(filename)
        with open(filename, "a") as f:
            df.to_csv(f, header=not file_exists, index=False)
        self.log.info("export_to_csv", f"Strategy output appended to {filename}")

    @staticmethod
    def generate_utx_id():
        return datetime.datetime.now().strftime("%Y%d%m%H%M%S%f")[:-3]
