<div align="Center">
    <h1>Yanagi Workbench</h1>
    <p><em>Python Automation Made Easy</em></p>
</div>

Yanagi Workbench is an open-source tool made purely in Python. It can do all the boring and repetitive tasks with just a few clicks, such as managing backups, transforming file formats of images/documents and the **CATS (Controlled Automatic Task Scheduler)** scheduler planned in a future release.


## Roadmap

The project follows [Semantic Versioning](https://semver.org/). Dragon names are release codenames; the numeric version remains the official way to identify compatibility and changes.

### v0.1.0 - Wyvern

Current development version.

- [x] Establish the desktop application structure
- [x] Add the home page and feature navigation
- [x] Add backup scheme
- [ ] Add image conversion
- [ ] Add file handling 
- [x] Implement settings section
- [ ] Check for possible bugs and release

### v0.2.0 - Drake

Add a notification system for task status, completion and errors
- [ ] Define notification levels for information, success, warning and error
- [ ] Create a reusable notification service for all application features
- [ ] Display notifications without interrupting the current workflow
- [ ] Include the task name, status and error details when applicable
- [ ] Add a way to dismiss or review recent notifications

Release the first version of CATS (Controlled Automatic Task Scheduler)
- [ ] Complete the core scheduler and interface workflows
- [ ] Test one-time and recurring tasks
- [ ] Test task persistence across application restarts
- [ ] Test notifications for completion, failure and cancellation
- [ ] Document how to create and manage scheduled tasks
- [ ] Mark CATS as ready for the Drake release

### v0.3.0 - Hydra

Expand Yanagi Workbench with data analysis capabilities.

- [ ] Integrate Pandas for data analysis workflows
- [ ] Integrate Openpyxl for Excel workbook processing
- [ ] Integrate NumPy for numerical operations
- [ ] Integrate SQLite for database manipulation
- [ ] Define the scope and name of the data analysis implementation
- [ ] Add interfaces for importing, processing and exporting data
- [ ] Document supported data formats and analysis workflows

Add a tabbed interface to manage multiple tasks simultaneously
- [ ] Define the layout and navigation behavior for tabs
- [ ] Create and close tabs without losing task state
- [ ] Associate each tab with an independent task or workflow
- [ ] Show the current task status in each tab
- [ ] Prevent unfinished work from being closed accidentally 

### v1.0.0 - Sea Dragon

First stable release.

- [ ] Improve the UI
- [ ] Review the workflows and fix possible bugs
- [ ] Make a general log system
- [ ] Publish the first stable release

The roadmap is intentionally flexible. Features may be moved between releases as implementation and testing provide better estimates.

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
sudo apt install python3-tk

# Install Python main dependencies
pip install -r requirements.txt
```

When activated, you can finally run the program by typing:
```bash
python3 run.py
```