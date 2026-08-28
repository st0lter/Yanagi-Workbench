"""
yanagiworkbench - A bootstack application.

Run with: python -m yanagiworkbench
"""

import bootstack as bs

from yanagiworkbench.pages.home_page import build_home
from yanagiworkbench.pages.settings_page import build_settings
from yanagiworkbench.pages.image_handler import build_image_handler
from yanagiworkbench.pages.backup_service import build_backup_service
from yanagiworkbench.pages.document_manager import build_document_manager

__version__ = "1.0.0 - Wyrm"


def main() -> None:
    """Application entry point."""
    with bs.AppShell(
        title="Yanagi Workbench",
        theme="dracula-dark",
        size=(1000, 650),
        show_statusbar=True,
    ) as shell:
        # --- Toolbar (menus + commands) -------------------------------------
        with shell.add_toolbar() as bar:
            with bar.add_menu("File") as file_menu:
                file_menu.add_action("Quit", shortcut="Mod+Q", on_click=shell.close)
            with bar.add_menu("Help") as help_menu:
                help_menu.add_action(
                    "About",
                    on_click=lambda: bs.alert("Thanks for using Yanagi Workbench!", title="About"),
                )
            bar.add_spacer()
            bar.add_theme_toggle()

        # --- Status bar -----------------------------------------------------
        shell.statusbar.add_text("Ready")
        shell.statusbar.add_text(f"v{__version__}", side="right")

        # --- Navigation: a flat sidebar of pages ----------------------------
        # Each page IS a layout container, so configure padding/gap/alignment on
        # add_page() and let the page's builder paint straight into it.
        with shell.page_nav() as nav:
            with nav.add_page("home", text="Home", icon="house",
                              padding=20, gap=12, horizontal_items="stretch"):
                build_home()

            with nav.add_page("imagehandler", text="Image Handler", icon="house",
                              padding=20, gap=12, horizontal_items="stretch"):
                build_image_handler()

            with nav.add_page("backup", text="Backup Service", icon="house",
                    padding=20, gap=12, horizontal_items="stretch"):
                build_backup_service()

            with nav.add_page("document", text="Document Manager", icon="house",
                    padding=20, gap=12, horizontal_items="stretch"):
                build_document_manager()

            with nav.add_page("settings", text="Settings", icon="gear",
                              pin_to_footer=True, padding=20, gap=12,
                              horizontal_items="stretch"):
                build_settings()

        shell.navigate("home")

    shell.run()


if __name__ == "__main__":
    main()
