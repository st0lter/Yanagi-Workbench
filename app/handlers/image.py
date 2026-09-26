from pathlib import Path

from PIL import Image, ImageOps

try:
    from pillow_heif import register_heif_opener
except ImportError:
    register_heif_opener = None

if register_heif_opener is not None:
    register_heif_opener()


class ImageHandler:
    def convert_image(self, original_image, output_path):
        original_image = Path(original_image)
        output_path = Path(output_path)

        with Image.open(original_image) as image:
            image = ImageOps.exif_transpose(image)
            if output_path.suffix.lower() in {'.jpg', '.jpeg'}:
                if image.mode not in {'RGB', 'L'}:
                    image = image.convert('RGB')
            elif image.mode == 'P' and 'transparency' in image.info:
                image = image.convert('RGBA')

            image.save(output_path)

        return output_path
