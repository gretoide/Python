import csv
from datetime import datetime
import os
from ...paths import RUTA_BASE

class EventLogger:
    def __init__(self):
        self.RUTA_LOG = os.path.join(RUTA_BASE, 'log')
        os.chdir(self.RUTA_LOG)
        self.log_file = os.path.join(self.RUTA_LOG, 'event_log.csv')

        self.create_log_file()

    def create_log_file(self):
        if not os.path.isfile(self.log_file):
            header = ['HORA', 'ALIAS', 'OPERACION', 'VALORES', 'TEXTOS']
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(header)

    def log_operation(self, alias, operation, values="", texts=""):
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        log_entry = [timestamp, alias, operation, values, texts]

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(log_entry)
