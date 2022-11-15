import os
import shutil

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_DIR = os.path.join(DIR_PATH, 'tmp_downloads\\')

def create_folder(dir_path, title):
    try:
        path_search_term = os.path.join(dir_path, title)
        os.mkdir(path_search_term)
        return True
    except Exception:
        print('Log: Folder "' + title + '" already exists.')
        return False


def move_file(source, destination):
    try:
        if os.path.isfile(source):
            shutil.move(source, destination)
            return True
    except Exception:
        return False

