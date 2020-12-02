import importlib.util
import mimetypes
import os

from pymocky.models.body_response import BodyResponse
from pymocky.utils.file import File
from pymocky.utils.log import Log


class MappingResponse(object):
    def __init__(self, mock_id, mock_scenario, data, base_path):
        self.mock_id = mock_id
        self.mock_scenario = mock_scenario

        self.base_path = base_path
        self.data = data

        self.status = self.data["status"] if "status" in self.data else 200
        self.headers = self.data.get("headers", {})
        self.body = BodyResponse(self.data, self.base_path)

        self.setup()

    def title(self):
        return os.path.join(self.base_path, self.body.file_name)

    def clear(self):
        self.status = 0
        self.headers = {}

    def body_file_path(self):
        return os.path.join(self.base_path, self.body.file_name)

    def setup(self):
        is_image = self.body.body_type == BodyResponse.IMAGE
        is_file = self.body.body_type == BodyResponse.FILE
        is_json = self.body.body_type == BodyResponse.JSON

        if is_image or is_file:
            full_path = self.body_file_path()

            if os.path.isfile(full_path):
                self.headers["Accept-Ranges"] = "bytes"
                self.headers["Pragma"] = "public"
                self.headers["Content-Length"] = os.path.getsize(full_path)

                mimetype = mimetypes.guess_type(full_path)

                if mimetype:
                    self.headers["Content-Type"] = mimetype[0]

                if is_file:
                    self.headers[
                        "Content-Disposition"
                    ] = 'attachment; filename="{0}"'.format(os.path.basename(full_path))
            else:
                Log.error("File not found: {0}".format(full_path), False)

                self.clear()
                self.status = 404
        elif is_json:
            self.headers["Content-Type"] = "application/json"

    def body_response(self):
        return self.body.read_value()

    def process_python_data(self, process_data):
        full_path = File.real_path(self.base_path, self.body.file_name)

        try:
            if os.path.isfile(full_path):
                # return a dict from python file
                module_name = File.get_filename_without_extension(full_path)
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                returned_data = module.run(process_data)

                # fill class with dict data
                self.status = (
                    returned_data["status"] if "status" in returned_data else 500
                )
                self.headers = (
                    returned_data["headers"] if "headers" in returned_data else {}
                )
                self.body.value = (
                    returned_data["body"] if "body" in returned_data else ""
                )
            else:
                Log.error("File not found: {0}".format(full_path), False)
                self.status = 404
        except Exception as e:
            Log.error(
                "Error when execute file {0}: {1}".format(full_path, repr(e)), False
            )

            self.status = 500
