"""Home page."""

import bootstack as bs


def build_home():
    """Build the Home page.

    A builder function: it paints into the active container. The page region
    (configured on `nav.add_page(...)` in main.py) supplies the padding and gap,
    so there is no extra layout wrapper here.
    """
    bs.Label("Welcome to yanagiworkbench", font="heading-xl")
    bs.Label(
        "This is your home page. Edit this file to get started.",
        wrap_width=500,
    )
    with bs.GroupBox("Getting Started", grow=True, horizontal="stretch"):
        bs.Label(
            "Add your widgets here.\n\n"
            "To add another page:\n"
            "  1. Run \'bootstack add page <Name>\' to generate the file.\n"
            "  2. In main.py, add a \'with nav.add_page(...):\' block inside\n"
            "     your \'shell.page_nav()\' and call the page's build_* function in it."
        )
