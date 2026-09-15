import shutil
import os
import datetime

def copy_folder(source, destination):
    shutil.copytree(source, destination)

def copy_files(source, destination):
    shutil.copy2(source, destination)
	
