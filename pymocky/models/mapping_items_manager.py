import yaml
from watchdog.observers import Observer

from pymocky.utils.file import File
from pymocky.utils.log import Log
from .config import Config
from .mapper_directory_listener import MapperDirectoryListener
from .mapping_item import *


class MappingItemsManager(object):
    event_handler = None
    yaml_files = None
    mappings = None

    def __init__(self):
        self.parse_yaml_files()

        if Config.watch:
            Log.info("Live reload enabled")
            self.install_watchers()

    def parse_yaml_files(self):
        self.yaml_files = File.get_yaml_files(Config.path)
        self.mappings = []

        for yaml_file in self.yaml_files:
            full_path = os.path.join(Config.path, yaml_file)

            with open(full_path, "r") as file:
                file_data = yaml.load(file, yaml.SafeLoader)

                if "mappings" in file_data:
                    mappings = file_data["mappings"]

                    if mappings and isinstance(mappings, list):
                        for mapping in mappings:
                            new_mapping = MappingItem(
                                mapping,
                                full_path,
                                os.path.dirname(full_path),
                            )

                            self.mappings.append(new_mapping)

        Log.info("Mappings loaded: {0:d}".format(len(self.mappings)))

    def response_for_mapping_request(self, request):
        return [
            item.response
            for item in self.mappings
            if item.handles_mapping_request(request)
        ]

    def mapping_item_for_mapping_request(self, request):
        # try find by scenario
        mappings = [
            item
            for item in self.mappings
            if item.mock_scenario == Config.scenario
            and item.handles_mapping_request(request)
        ]

        if mappings:
            if Config.verbose:
                Log.info("Mapping found by scenario: {0}".format(Config.scenario))

            return mappings

        # try find by default scenario
        mappings = [
            item
            for item in self.mappings
            if item.mock_scenario == Constants.DEFAULT_SCENARIO
            and item.handles_mapping_request(request)
        ]

        if mappings:
            if Config.verbose:
                Log.info("Mapping found by default scenario")

            return mappings

        return []

    def install_watchers(self):
        self.event_handler = MapperDirectoryListener(self)
        self.install_watcher(Config.path)

    def install_watcher(self, path):
        observer = Observer()
        observer.schedule(self.event_handler, path, recursive=True)
        observer.start()
