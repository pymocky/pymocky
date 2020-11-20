import os
import uuid
from os.path import basename

from .constants import Constants
from .mapping_request import MappingRequest
from .mapping_response import MappingResponse


class MappingItem(object):
    def __init__(self, data, file_name, base_path):
        self.mock_id = self.get_id(data)
        self.mock_scenario = self.get_scenario(data)

        self.request = MappingRequest(
            self.mock_id,
            self.mock_scenario,
            data["request"],
        )

        self.response = MappingResponse(
            self.mock_id,
            self.mock_scenario,
            data["response"],
            base_path,
        )

        self.file_name = file_name
        self.display_name = self.get_display_name(data, file_name)

    @staticmethod
    def get_id(dic):
        result = ""

        if "id" in dic:
            result = dic["id"]

        if len(result) == 0:
            result = uuid.uuid4()

        return result

    @staticmethod
    def get_scenario(dic):
        result = ""

        if "scenario" in dic:
            result = dic["scenario"]

        if len(result) == 0:
            result = Constants.DEFAULT_SCENARIO

        return result

    @staticmethod
    def get_display_name(dic, file_name):
        if "name" in dic:
            return dic["name"]
        else:
            return os.path.splitext(basename(file_name))[0]

    def handles_mapping_request(self, other_request):
        return self.request == other_request
