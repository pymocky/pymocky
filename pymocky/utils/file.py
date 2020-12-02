import os
import re
import shutil
import sys
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

        result = os.path.expanduser(result)
        result = os.path.expandvars(result)
        result = Path(result)

        if sys.version_info < (3, 6):
            return str(result.absolute())
        else:
            return str(result.resolve().absolute())

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

    @staticmethod
    def get_filename_without_extension(file_path):
        path = Path(file_path)
        return path.stem
