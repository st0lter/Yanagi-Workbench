import os
import shutil
import datetime
from threading import Event

class BackupHandler:
    def backup(self, source, destination, source_type, on_progress, cancel_event, on_started=None):
        # Create a separate timestamped folder for each backup operation.
        backup_name = datetime.datetime.now().strftime('BACKUP-%Y-%m-%d_%H:%M:%S')
        backup_destination = os.path.join(destination, backup_name)
        os.makedirs(backup_destination, exist_ok=True)

        if on_started:
            on_started(self._count_files(source, source_type))

        if source_type == 'Folder':
            folder_source = source[0] if not isinstance(source, (str, bytes, os.PathLike)) else source
            return self.copy_folder(folder_source, backup_destination, on_progress, cancel_event)
        return self.copy_files(source, backup_destination, on_progress, cancel_event)

    @staticmethod
    def _count_files(source, source_type):
        if source_type != 'Folder':
            return len(source) if not isinstance(source, (str, bytes, os.PathLike)) else 1

        sources = (source,) if isinstance(source, (str, bytes, os.PathLike)) else source
        return sum(
            len(files)
            for source_root in sources
            for _, _, files in os.walk(source_root)
        )

    def copy_folder(self, source, destination, on_progress, cancel_event=None):
        cancel_event = cancel_event or Event()
        # Keep the original folder name inside the timestamped backup folder.
        target = os.path.join(destination, os.path.basename(os.path.normpath(source)))

        for root, directories, files in os.walk(source):
            if cancel_event.is_set():
                return False

            relative_root = os.path.relpath(root, source)
            target_root = target if relative_root == '.' else os.path.join(target, relative_root)
            os.makedirs(target_root, exist_ok=True)

            for file_name in files:
                if cancel_event.is_set():
                    return False
                source_file = os.path.join(root, file_name)
                destination_file = os.path.join(target_root, file_name)
                # Report each file before copying it so the UI can update the log.
                on_progress(source_file, destination_file)
                shutil.copy2(source_file, destination_file)

        return True

    def copy_files(self, source, destination, on_progress, cancel_event=None):
        cancel_event = cancel_event or Event()
        sources = (source,) if isinstance(source, (str, bytes, os.PathLike)) else source

        # Copy every selected file into the same timestamped backup folder.
        for source_file in sources:
            if cancel_event.is_set():
                return False
            destination_file = os.path.join(destination, os.path.basename(source_file))
            on_progress(source_file, destination_file)
            shutil.copy2(source_file, destination_file)
        return True
