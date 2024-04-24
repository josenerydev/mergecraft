import os
import tempfile
import subprocess
import pathspec
import argparse
import re
import yaml


def load_config():
    """Load configuration from a YAML file."""
    config_path = os.path.join(os.getcwd(), "mergecraft.config.yml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "Could not find the configuration file 'mergecraft.config.yml'."
        )
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


config = load_config()


def find_subdir(start_dir, subdir_name):
    """Recursively search for a subdirectory within the start directory."""
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for dirname in dirnames:
            if subdir_name in dirname:
                return os.path.join(dirpath, dirname)
    return None


def read_file_content(filepath):
    """Read the content of a file."""
    with open(filepath, "rb") as file:
        content_bytes = file.read()
        content = content_bytes.decode("utf-8", errors="replace")
        return content if content.strip() else "(empty)"


def load_gitignore():
    """Load the .gitignore specifications."""
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            gitignore = f.readlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", gitignore)
    return None


def should_skip_filename(filename):
    """Check if file should be skipped based on config."""
    for pattern in config["skip_files"]:
        if re.match(pattern.replace("*", ".*"), filename):
            return True
    return False


def should_skip_directory(dirpath):
    """Return True if the directory should be skipped based on config."""
    return any(
        skip_dir in dirpath.split(os.path.sep)
        for skip_dir in config["skip_directories"]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Merge files into a temporary file and open in VS Code."
    )
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=config.get("extensions", [".py"]),
        help="Specify the file extensions to process.",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Specify the root path to start searching for files. Defaults to current directory.",
    )
    parser.add_argument(
        "--filter",
        help="A regex pattern to filter files based on their content or name.",
    )
    args = parser.parse_args()

    full_path = os.path.normpath(os.path.join(os.getcwd(), args.path))
    if not os.path.exists(full_path):
        full_path = find_subdir(os.getcwd(), args.path)

    if not full_path or not os.path.exists(full_path):
        print(f"Error: The specified path '{args.path}' was not found.")
        return

    with tempfile.NamedTemporaryFile(prefix="mergecraft_", delete=False) as temp_file:
        temp_path = temp_file.name

    gitignore_spec = load_gitignore()
    read_files = []
    total_line_count = 0

    for dirpath, dirnames, filenames in os.walk(full_path):
        if ".git" in dirpath or should_skip_directory(dirpath):
            continue

        for filename in filenames:
            if should_skip_filename(filename):
                continue

            if not any(filename.endswith(ext) for ext in args.extensions):
                continue

            filepath = os.path.join(dirpath, filename)
            if gitignore_spec and gitignore_spec.match_file(
                os.path.relpath(filepath, start=os.getcwd())
            ):
                continue

            content = read_file_content(filepath)
            if args.filter and not (
                re.search(args.filter, content) or re.search(args.filter, filename)
            ):
                continue

            line_count = len(content.split("\n"))
            total_line_count += line_count
            read_files.append((filepath, line_count))

            with open(filepath, "r", encoding="utf-8") as original_file:
                file_content = original_file.read()

            with open(temp_path, "a", encoding="utf-8") as temp_file:
                temp_file.write(f"# {filepath}\n{file_content}\n")

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
