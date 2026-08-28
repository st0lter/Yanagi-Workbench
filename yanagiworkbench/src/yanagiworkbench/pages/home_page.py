"""Home page."""

import bootstack as bs


def build_home():
    """Build the Home page.

    A builder function: it paints into the active container. The page region
    (configured on `nav.add_page(...)` in main.py) supplies the padding and gap,
    so there is no extra layout wrapper here.
    """
    bs.Label("Welcome to Yanagi Workbench", font="heading-xl")
    bs.Label(
        "Here are some steps for you to get started!",
        wrap_width=500,
    )
    with bs.GroupBox("Getting Started", grow=True, horizontal="stretch"):
        bs.Label(
            "\n\n"
            "On the sidebard, you can find the tabs that will guide you to each section\n"
            "Each tab will have their own functonalities, for example:\n"
            "\n"
            ">>> Image Handler - It will manage image operations, such as format conversion and resizing, for example\n"
            ">>> Backup - It handles backup file operations for folders and files\n"
            ">>> Document Manager - It is able to manage PDF/DOCX documents operations."
        )
