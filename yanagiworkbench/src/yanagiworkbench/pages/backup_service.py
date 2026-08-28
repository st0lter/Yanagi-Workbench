"""Backup page."""

import bootstack as bs


def build_backup_service():
    """Build the Backup page."""
    bs.Label("Backup", font="heading-lg")
    with bs.GroupBox("Content", grow=True, horizontal="stretch"):
        pass  # Add your widgets here
