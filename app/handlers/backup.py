"""Backup actions for the backup page."""

from datetime import datetime
from pathlib import Path
import shutil
import threading
from tkinter import filedialog


class BackupHandler:
	def __init__(self, page):
		self.page = page
		page.origin_btn.configure(command=self.select_origin)
		page.destination_btn.configure(command=self.select_destination)
		page.backup_btn.configure(command=self.start_backup)

	@staticmethod
	def _set_entry(entry, value):
		entry.configure(state="normal")
		entry.delete(0, "end")
		entry.insert(0, value)
		entry.configure(state="readonly")

	def select_origin(self):
		"""Select multiple files or a single folder."""
		files = filedialog.askopenfilenames(title="Select files for backup")
		if files:
			self._set_entry(self.page.origin_path, "|".join(files))
			return

		directory = filedialog.askdirectory(title="Select a folder for backup")
		if directory:
			self._set_entry(self.page.origin_path, directory)

	def select_destination(self):
		directory = filedialog.askdirectory(title="Select the backup destination")
		if directory:
			self._set_entry(self.page.destination_path, directory)

	def _log(self, message):
		self.page.after(0, self._append_log, message)

	def _append_log(self, message):
		self.page.backup_log.configure(state="normal")
		self.page.backup_log.insert("end", message + "\n")
		self.page.backup_log.see("end")
		self.page.backup_log.configure(state="disabled")

	def _set_backup_button_state(self, state):
		self.page.backup_btn.configure(state=state)

	def start_backup(self):
		source_text = self.page.origin_path.get().strip()
		destination_text = self.page.destination_path.get().strip()
		sources = [Path(item) for item in source_text.split("|") if item]

		if not sources or not all(path.exists() for path in sources):
			self._log("Select a valid folder or file for backup.")
			return
		if not destination_text:
			self._log("Select a valid output directory.")
			return

		destination = Path(destination_text)
		if not destination.is_dir():
			self._log("Select a valid output directory.")
			return

		timestamp = datetime.now().strftime("%H-%M-%S-%d_%m_%Y")
		backup_dir = destination / f"Backup-{timestamp}"
		self._set_backup_button_state("disabled")
		threading.Thread(
			target=self._run_backup,
			args=(sources, destination, backup_dir),
			daemon=True,
		).start()

	def _run_backup(self, sources, destination, backup_dir):
		try:
			backup_dir.mkdir()
			for source in sources:
				item_type = "pasta" if source.is_dir() else "arquivo"
				self._log(f"Copying {item_type} {source} to {destination}")
				target = backup_dir / source.name
				if source.is_dir():
					shutil.copytree(source, target)
				else:
					shutil.copy2(source, target)
		except (OSError, shutil.Error) as error:
			shutil.rmtree(backup_dir, ignore_errors=True)
			self._log(f"Backup error: {error}")
		else:
			self._log(f"Backup created successfully at: {backup_dir}")
		finally:
			self.page.after(0, self._set_backup_button_state, "normal")


def setup(page):
	"""Attach this handler to an existing BackupPage instance."""
	return BackupHandler(page)
