import os
import tempfile
import subprocess
import pathspec
import argparse
import re


def find_subdir(start_dir, subdir_name):
    """Recursively search for a subdirectory within the start directory."""
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for dirname in dirnames:
            if subdir_name in dirname:
                # print(f"Found directory: {os.path.join(dirpath, dirname)}")  # Debug
                return os.path.join(dirpath, dirname)
    # print(
    #     f"Directory '{subdir_name}' not found from starting point: {start_dir}"
    # )  # Debug
    return None


def read_file_content(filepath):
    """Read the content of a file."""
    with open(filepath, "rb") as file:
        content_bytes = file.read()
        content = content_bytes.decode("utf-8", errors="replace")
        return content if content.strip() else "(empty)"


def load_gitignore():
    """Load the .gitignore specifications."""
    with open(".gitignore", "r") as f:
        gitignore = f.readlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", gitignore)


def should_skip_directory(dirpath):
    """Return True if the directory should be skipped based on certain criteria."""
    skip_directories = ["bin", "obj", ".git"]
    for skip_dir in skip_directories:
        if skip_dir in dirpath.split(os.path.sep):
            return True
    return False


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Merge files into a temporary file and open in VS Code."
    )
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=None,  # Default para None, vamos tratar isso mais adiante
        help="Specify the file extensions to process.",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Specify the root path to start searching for files. Defaults to current directory.",
    )
    parser.add_argument(
        "--filter",
        help="A regex pattern to filter files based on their content or name. Only files matching this pattern will be included.",
    )
    args = parser.parse_args()

    # Se --path for fornecido e --extensions não for, leremos todos os arquivos
    if args.path != "." and args.extensions is None:
        args.extensions = [""]
    elif args.filter != "" and args.extensions is None:
        args.extensions = [""]
    elif (
        args.extensions is None
    ):  # Se --extensions não for fornecido, vamos usar .py como padrão
        args.extensions = [".py"]

    # Validate Regex
    if args.filter:
        try:
            re.compile(args.filter)
        except re.error:
            print("Error: Invalid regular expression provided!")
            return

    # If no extensions are explicitly provided, default to .py
    if args.extensions is None:
        args.extensions = [".py"]

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

    gitignore_spec = load_gitignore() if os.path.exists(".gitignore") else None

    read_files = []
    total_line_count = 0

    for dirpath, dirnames, filenames in os.walk(full_path):
        # Debug
        # print(f"Checking directory: {dirpath}")

        # Ignore the .git directory
        if ".git" in dirpath:
            # print("Skipping .git directory")  # Debug
            continue

        for filename in filenames:
            # Check if filename is .gitignore
            if filename in [".gitignore", "LICENSE", "README.md", "__init__.py"]:
                continue

            # Filter by extensions
            if not filename.endswith(tuple(args.extensions)):
                continue

            filepath = os.path.join(dirpath, filename)
            relative_filepath = os.path.relpath(filepath)

            # Check against gitignore rules
            if gitignore_spec and gitignore_spec.match_file(relative_filepath):
                # print(f"File {filepath} is ignored due to .gitignore rules.")
                continue

            # Apply the filter to both filename and content
            content = read_file_content(filepath)
            if args.filter and not (
                re.search(args.filter, content) or re.search(args.filter, filename)
            ):
                # print(f"File {filepath} does not match the provided filter.")  # Debug
                continue

            line_count = len(content.split("\n"))
            total_line_count += line_count
            read_files.append((relative_filepath, line_count))

            with open(filepath, "r", encoding="utf-8") as original_file:
                content = original_file.read()

            with open(temp_path, "a", encoding="utf-8") as temp_file:
                temp_file.write(f"# {filepath}\n{content}\n")

    print("Editing in VS Code. Close to continue.")
    subprocess.run(["cmd", "/c", "code", "-w", temp_path])

    if not read_files:
        print("No files were read!")
        return

    print("Editing completed. Continuing script execution...")
    print("\nSummary:")
    print(f"Total files read: {len(read_files)}")
    print(f"Total lines: {total_line_count}")
    print("\nFiles read:")
    for file_path, line_count in read_files:
        print(f"{file_path}: {line_count} lines")

    os.remove(temp_path)


if __name__ == "__main__":
    main()
