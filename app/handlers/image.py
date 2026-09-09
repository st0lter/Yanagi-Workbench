from pathlib import Path
import threading

from PIL import Image

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass


class ImageHandler:
    def __init__(self, origin_path, destination_path, origin_format, destination_format):
        paths = origin_path if isinstance(origin_path, (list, tuple)) else [origin_path]
        self.origin_paths = [Path(path) for path in paths]
        self.destination_path = Path(destination_path)
        self.origin_format = self._extension(origin_format)
        self.destination_format = self._extension(destination_format)

    def convert_images(self, on_message=None, on_progress=None):
        self.destination_path.mkdir(parents=True, exist_ok=True)
        messages = []
        files_to_convert = [
            file_path
            for origin_path in self.origin_paths
            for file_path in self._source_files(origin_path)
            if self._matches_origin_format(file_path.name)
        ]

        for index, origin_file_path in enumerate(files_to_convert, start=1):
            file_name = origin_file_path.name
            destination_file_name = f"{origin_file_path.stem}_converted.{self.destination_format}"
            destination_file_path = self.destination_path / destination_file_name

            try:
                with Image.open(str(origin_file_path)) as img:
                    if self.destination_format in {"jpg", "jpeg"} and img.mode in {"RGBA", "LA", "P"}:
                        img = img.convert("RGB")
                    img.save(str(destination_file_path))
                message = f"{file_name} has been converted to {destination_file_name}"
            except Exception as error:
                message = f"Failed to convert {file_name}: {error}"
            messages.append(message)
            if on_message:
                on_message(message)
            if on_progress:
                on_progress(index, len(files_to_convert))

        if not messages:
            message = f"No .{self.origin_format} images found"
            messages.append(message)
            if on_message:
                on_message(message)
        return messages

    def convert_images_async(self, on_complete=None, on_message=None, on_progress=None):
        threading.Thread(
            target=self._convert_images_in_background,
            args=(on_complete, on_message, on_progress),
            daemon=True,
        ).start()

    def _convert_images_in_background(self, on_complete, on_message, on_progress):
        try:
            messages = self.convert_images(on_message, on_progress)
        except Exception as error:
            messages = [f"Conversion failed: {error}"]
            if on_message:
                on_message(messages[0])
        if on_complete:
            on_complete(messages)

    @staticmethod
    def _source_files(origin_path):
        if origin_path.is_dir():
            return (file_path for file_path in origin_path.rglob("*") if file_path.is_file())
        return (origin_path,)

    @staticmethod
    def _extension(image_format):
        return {"jpeg": "jpg", "heic/heif": "heic"}.get(image_format.lower(), image_format.lower())

    def _matches_origin_format(self, file_name):
        extensions = {"heic": (".heic", ".heif")}.get(self.origin_format, (f".{self.origin_format}",))
        return file_name.lower().endswith(extensions)