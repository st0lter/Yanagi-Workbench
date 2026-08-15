APP_THEME = {
    "default_mode": "dark",
    "light": {
        "primary": "#1F6FB2",
        "danger": "#C1121F",
        "success": "#0B8A3A",
        "text": "#2B2B2B",
        "panel": "#EAEAEA",
        "surface": "#F5F5F5",
        "sidebar_bg": "#D9D9D9",
        "button_text": "#FFFFFF",
        "log_default": "#2B2B2B",
        "log_info": "#1F6FB2",
        "log_error": "#C1121F",
        "log_success": "#0B8A3A",
        "log_message": "#1A5D7B",
    },
    "dark": {
        "primary": "#0D6EFD",
        "danger": "#D90429",
        "success": "#0CCA4A",
        "text": "#EDF2F4",
        "panel": "#2B2B2B",
        "surface": "#1B1B1B",
        "sidebar_bg": "#2A2F38",
        "button_text": "#FFFFFF",
        "log_default": "#EDF2F4",
        "log_info": "#2374AB",
        "log_error": "#D90429",
        "log_success": "#0CCA4A",
        "log_message": "#9CFFD9",
    },
}


def get_theme_palette(mode: str = None):
    selected_mode = (mode or APP_THEME["default_mode"]).lower()
    return APP_THEME.get(selected_mode, APP_THEME["dark"]).copy()
