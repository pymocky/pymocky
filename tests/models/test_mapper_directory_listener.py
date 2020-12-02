import os
import unittest
from io import StringIO
from unittest.mock import patch

from watchdog.observers import Observer

from pymocky.models.config import Config
from pymocky.models.mapper_directory_listener import MapperDirectoryListener
from pymocky.models.mapping_items_manager import MappingItemsManager
from pymocky.utils.file import File


class MapperDirectoryListenerTests(unittest.TestCase):
    def test_event_listener(self):
        with patch("sys.stdout", new=StringIO()) as output:
            path = os.path.join(os.getcwd(), "extras", "sample")

            Config.init_from_args_dict(
                {
                    "verbose": True,
                    "path": path,
                }
            )

            handler = MappingItemsManager()
            event_handler = MapperDirectoryListener(handler)

            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()

            file_path = os.path.join(path, "files.yml")
            content = File.get_file_content(file_path)
            File.write_to_file(path, "files.yml", content)

            self.assertIn("Mappings loaded: 13", output.getvalue().strip())
