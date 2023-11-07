import os, yaml
from datetime import datetime

def get_unique_time_id() -> str:
    return\
        str(datetime.now()).\
        replace('-', '').\
        replace(':', '').\
        replace('.', '').\
        replace(' ', '').\
        strip()

def clean_up_folder(target: str) -> None:
    files = os.listdir(target)
    for file in files:
        file_path = os.path.join(target, file)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                return e