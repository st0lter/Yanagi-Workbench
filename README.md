<div align="Center">
    <h1>Yanagi Workbench</h1>
    <p><em>Python Automation Made Easy</em></p>
</div>

Yanagi Workbench is an open-source tool made purely in Python. It can do all the boring and repetitive tasks with just a few clicks, such as managing backups, transforming file formats of images/documents and also, scheduling tasks with **CATS (Controlled Automatic Task Scheduler)**.

## System dependencies
Some libraries used in the program may need to be installed in order for it to work properly.

But first of all, make sure to create a virtual environment.
```bash
# Creates the virtual environment
python3 -m venv .venv

# Activates the environment
source .venv/bin/activate
```

After activating, paste these commands below on the terminal.
```bash
# Install system dependencies
sudo apt install pandoc

# Install Python main dependencies
pip install ttkbootstrap pypandoc pypdf
```

When activated, you can finally run the program by typing:
```bash
python3 run.py
```