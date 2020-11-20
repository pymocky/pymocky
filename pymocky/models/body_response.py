import json
import os

from pymocky.utils.file import File


class BodyResponse(object):
    NONE = "none"
    RAW = "raw"
    IMAGE = "image"
    FILE = "file"
    JSON = "json"

    @property
    def body_type(self):
        return self._body_type

    def __init__(self, dic, base_path):
        self.base_path = base_path
        self.value = ""
        self._body_type = BodyResponse.NONE

        if dic:
            if "body_raw" in dic:
                self._body_type = BodyResponse.RAW
                self.file_name = ""
                self.value_from_raw(dic["body_raw"])

            elif "body_file" in dic:
                self._body_type = BodyResponse.FILE
                self.file_name = dic["body_file"]
                self.value_from_file(self.file_name)

            elif "body_image" in dic:
                self._body_type = BodyResponse.IMAGE
                self.file_name = dic["body_image"]
                self.value_from_image(self.file_name)

            elif "body_json" in dic:
                self._body_type = BodyResponse.JSON
                self.file_name = ""
                self.value_from_object(dic["body_json"])

    def read_value(self):
        if callable(self.value):
            return self.value()
        else:
            return self.value

    def value_from_file(self, file):
        self.value = lambda: self.read_file(file)

    def value_from_object(self, obj):
        if isinstance(obj, str):
            self.value = lambda: json.dumps(obj)

        elif isinstance(obj, dict) or isinstance(obj, list):
            self.value = lambda: json.dumps(obj)

    def value_from_raw(self, obj):
        if isinstance(obj, str):
            self.value = obj
        else:
            self.value = ""

    def value_from_image(self, image):
        self.value = lambda: self.read_file(image)

    def read_file(self, path):
        full_path = File.real_path(self.base_path, path)

        if os.path.isfile(full_path):
            with open(full_path, "rb") as file:
                content = file.read()
                return content
        else:
            return None
