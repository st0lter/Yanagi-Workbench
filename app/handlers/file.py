from pathlib import Path
import platform
import shutil
import subprocess

from docx2pdf import convert
from pdf2docx import Converter


class FileHandler:
    def __init__(self):
        self.system = platform.system()  # "Windows", "Darwin" (macOS) or "Linux"

    def convert_pdf_to_docx(self, pdf_file, docx_path):
        pdf_file = Path(pdf_file)
        docx_path = Path(docx_path)
        converter = Converter(str(pdf_file))
        try:
            converter.convert(str(docx_path))
        finally:
            converter.close()
        return docx_path

    def convert_docx_to_pdf(self, docx_file, pdf_path):
        docx_file = Path(docx_file)
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        if self.system in ('Windows', 'Darwin'):
            convert(str(docx_file), str(pdf_path))
            return pdf_path

        # If MS Word is not installed, it falls here
        else:
            soffice = shutil.which("soffice") or shutil.which("libreoffice")

            # If not even LibreOffice is found, returns error message
            if soffice is None:
                raise RuntimeError('Neither MS Word nor LibreOffice is available.')

            subprocess.run(
                [soffice, '--headless', '--convert-to', 'pdf',
                 '--outdir', str(pdf_path.parent), str(docx_file)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            generated_path = pdf_path.parent / f'{docx_file.stem}.pdf'
            if not generated_path.exists():
                raise FileNotFoundError(f'LibreOffice did not create {generated_path}.')
            return generated_path
