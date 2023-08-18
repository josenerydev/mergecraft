import os
import tempfile
import subprocess
import pathspec
import argparse


def find_subdir(start_dir, subdir_name):
    """
    Recursively search for a subdirectory within the start directory.
    """
    for dirpath, dirnames, filenames in os.walk(start_dir):
        if os.path.basename(dirpath) == subdir_name:
            return dirpath
    return None


def read_file_content(filepath):
    """Read the content of a file."""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        return content if content.strip() else "(empty)"


def load_gitignore():
    """Load the .gitignore specifications."""
    with open(".gitignore", "r") as f:
        gitignore = f.readlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", gitignore)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Merge files into a temporary file and open in VS Code."
    )

    ext_help = """
    Specify the file extensions to process. 
    You can provide multiple extensions by separating them with spaces.
    Example:
        mergecraft -e .py .txt
        This will process both Python and TXT files.
    If not provided, the tool defaults to processing .py files.
    """
    parser.add_argument(
        "-e", "--extensions", nargs="+", default=[".py"], help=ext_help.strip()
    )

    # Add argument for specifying the path
    parser.add_argument(
        "--path",
        default=".",
        help="Specify the root path to start searching for files. Defaults to current directory.",
    )
    args = parser.parse_args()

    # Normalize the path and check if it exists
    current_dir = os.getcwd()
    full_path = os.path.normpath(os.path.join(current_dir, args.path))

    if not os.path.exists(full_path):
        # If the path doesn't exist directly, try to find it recursively
        full_path = find_subdir(current_dir, args.path)

    if not full_path or not os.path.exists(full_path):
        print(
            f"Error: The specified path '{args.path}' was not found in '{current_dir}' or its subdirectories!"
        )
        return

    # Create a temporary file with a meaningful prefix
    with tempfile.NamedTemporaryFile(prefix="mergecraft_", delete=False) as temp_file:
        temp_path = temp_file.name

    # Check if .gitignore exists and load its rules
    gitignore_spec = None
    if os.path.exists(".gitignore"):
        gitignore_spec = load_gitignore()

    # Create a list to store the names of the read files
    read_files = []

    # Iterate over the files starting from the full path
    for dirpath, dirnames, filenames in os.walk(full_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            relative_filepath = os.path.relpath(
                filepath
            )  # get path relative to current directory

            # Check against gitignore rules
            if gitignore_spec and gitignore_spec.match_file(relative_filepath):
                continue  # Skip this file

            # If the user has specified a path, consider all files inside that path
            # Otherwise, use the extensions filter
            if args.path != "." or any(
                filename.endswith(ext) for ext in args.extensions
            ):
                # Add the file to the list of read files
                read_files.append(relative_filepath)

                content = read_file_content(filepath)
                with open(temp_path, "a", encoding="utf-8") as temp_file:
                    temp_file.write(f"``` {filename}\n{content}\n```\n\n")

    print("Editing in VS Code. Close to continue.")

    # Open the temporary file in VS Code
    subprocess.run(["cmd", "/c", "code", "-w", temp_path])

    # Check if no files were read
    if not read_files:
        print("No files were read!")
        return

    print("Editing completed. Continuing script execution...")

    # Print the list of read files
    print("\nFiles read:")
    for file in read_files:
        print(file)

    # Remove the temporary file
    os.remove(temp_path)


if __name__ == "__main__":
    main()
