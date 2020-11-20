import os
import re
import shutil
from pathlib import Path

import regex


class File(object):
    @staticmethod
    def get_yaml_files(path):
        files = os.listdir(path)
        return filter(lambda file: re.match(r".*\.yml$", file), files)

    @staticmethod
    def real_path(base_path, path):
        result = ""

        if path:
            if path.startswith("//"):
                if base_path:
                    path = regex.sub("//", "", path, 1)
                    result = os.path.join(base_path, path)
                else:
                    result = regex.sub("//", "", path, 1)
            else:
                if base_path:
                    result = os.path.join(base_path, path)
                else:
                    result = path

        result = Path(os.path.expandvars(result))

        return str(result.absolute())

    @staticmethod
    def write_to_file(dirname, filename, content):
        full_file_path = os.path.join(dirname, filename)
        File.remove_file(full_file_path)
        File.create_dir(dirname)

        with open(full_file_path, "w") as f:
            f.write(content)
            f.close()

    @staticmethod
    def get_file_content(file):
        file = open(file, mode="r")
        content = file.read()
        file.close()
        return content

    @staticmethod
    def remove_dir(dir_path):
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def create_dir(dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def remove_file(filename):
        if os.path.isfile(filename):
            os.remove(filename)
