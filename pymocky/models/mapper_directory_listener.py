from watchdog.events import FileSystemEventHandler

from pymocky.utils.log import Log


class MapperDirectoryListener(FileSystemEventHandler):
    def __init__(self, mapping_manager):
        self.mapping_manager = mapping_manager

    def on_any_event(self, event):
        Log.info(
            "Directory changed, rebuilding mapping settings...\n"
            "Path: %s" % event.src_path + "\nEvent type: %s" % event.event_type
        )

        self.mapping_manager.parse_yaml_files()

        Log.ok("Mapping settings rebuilt successfully")
