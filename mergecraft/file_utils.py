import os

def find_subdir(start_dir, subdir_name):
    """Recursively search for a subdirectory within the start directory."""
    for dirpath, dirnames, _ in os.walk(start_dir):
        for dirname in dirnames:
            if subdir_name in dirname:
                return os.path.join(dirpath, dirname)
    return None

def read_file_content(filepath):
    """Read the content of a file."""
    with open(filepath, "rb") as file:
        content_bytes = file.read()
        return content_bytes.decode("utf-8", errors="replace").strip() or "(empty)"
