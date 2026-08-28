"""Settings page."""

import bootstack as bs


def build_settings():
    """Build the Settings page."""
    bs.Label("Settings", font="heading-xl")
    bs.Label("Configure your application preferences.", wrap_width=500)
    with bs.GroupBox("Preferences", grow=True, horizontal="stretch"):
        with bs.Row(gap=8):
            bs.Label("Theme:")
            bs.ThemeToggle()
