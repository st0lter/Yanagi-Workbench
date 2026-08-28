"""Document Manager page."""

import bootstack as bs


def build_document_manager():
    """Build the Document Manager page."""
    bs.Label("Document Manager", font="heading-lg")
    with bs.GroupBox("Content", grow=True, horizontal="stretch"):
        pass  # Add your widgets here
