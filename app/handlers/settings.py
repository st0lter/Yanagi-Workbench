import configparser
import platformdirs
from pathlib import Path

from app.config import MIN_HEIGHT, MIN_WIDTH, THEMES


DEFAULT_THEME = 'tokyo-night-dark'

class Settings:
    def __init__(self, filename='config.ini'):
        app_dir = Path(platformdirs.user_config_dir('YanagiWorkbench'))
        app_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = app_dir / filename
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if self.filepath.exists():
            self.config.read(self.filepath)
        self._set_default('WINDOW', 'WIDTH', MIN_WIDTH)
        self._set_default('WINDOW', 'HEIGHT', MIN_HEIGHT)
        self._set_default('APP', 'THEME', DEFAULT_THEME)
        self._set_default('APP', 'NOTIFICATIONS', 'false')
        self.save_file()

    def _set_default(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        if not self.config.has_option(section, key):
            self.config.set(section, key, value)

    @property
    def theme(self):
        theme = self.config.get('APP', 'THEME', fallback=DEFAULT_THEME)
        valid_themes = set(THEMES.values())
        return theme if theme in valid_themes else DEFAULT_THEME

    @property
    def window_size(self):
        width = self.config.get('WINDOW', 'WIDTH', fallback=MIN_WIDTH)
        height = self.config.get('WINDOW', 'HEIGHT', fallback=MIN_HEIGHT)
        return f'{width}x{height}'

    @property
    def notifications(self):
        return self.config.getboolean('APP', 'NOTIFICATIONS', fallback=False)

    def update(self, *, theme=None, window_size=None, notifications=None):
        if theme is not None and theme in THEMES.values():
            self.config.set('APP', 'THEME', theme)
        if window_size is not None:
            width, separator, height = window_size.partition('x')
            if separator and width.isdigit() and height.isdigit():
                self.config.set('WINDOW', 'WIDTH', width)
                self.config.set('WINDOW', 'HEIGHT', height)
        if notifications is not None:
            self.config.set('APP', 'NOTIFICATIONS', str(bool(notifications)).lower())
        self.save_file()

    def save_file(self):
        with self.filepath.open('w', encoding='utf-8') as file:
            self.config.write(file)
        