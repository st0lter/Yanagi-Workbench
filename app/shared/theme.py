from app.config.theme_config import get_theme_palette


def get_msg_colors(mode: str = "dark"):
    palette = get_theme_palette(mode)
    return {
        "info": palette["log_info"],
        "error": palette["log_error"],
        "success": palette["log_success"],
        "message": palette["log_message"],
        "default": palette["log_default"],
    }


MSG_COLORS = get_msg_colors("dark")
LIGHT_MSG_COLORS = get_msg_colors("light")
