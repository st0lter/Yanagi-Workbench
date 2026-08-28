# yanagiworkbench

A bootstack application using AppShell navigation.

## Getting Started

### Development

```bash
# Run the application
python -m yanagiworkbench

# Or use the CLI
bootstack run
```

### Adding Pages

```bash
# Scaffold a new page
bootstack add page DashboardPage

# Then wire it up in main.py, inside your shell.page_nav() block:
#   from yanagiworkbench.pages.dashboard_page import build_dashboard
#   with nav.add_page("dashboard", text="Dashboard", icon="speedometer2",
#                     padding=20, gap=12, horizontal_items="stretch"):
#       build_dashboard()
```

### Building for Distribution

```bash
# Promote to packaging-ready (adds PyInstaller support)
bootstack promote --pyinstaller

# Build the executable
bootstack build
```

## Project Structure

```
yanagiworkbench/
├── src/yanagiworkbench/
│   ├── __init__.py
│   ├── main.py
│   └── pages/
│       ├── __init__.py
│       ├── home_page.py
│       └── settings_page.py
├── assets/
├── bootstack.toml
└── README.md
```

## Configuration

Application settings are defined in `bootstack.toml`:

- `[app]` - Application metadata
- `[layout]` - Default layout preferences
- `[build]` - Build/packaging configuration (after `bootstack promote`)
