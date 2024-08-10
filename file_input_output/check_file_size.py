'''
Logical error to fix
'''

import os

def has_file_size_changed(file_name):
    previous_size = None
    current_size = os.path.getsize(f"C:\\Users\\Path_Here")

    if previous_size is not None:
        if current_size != previous_size:
            previous_size = current_size

            return True