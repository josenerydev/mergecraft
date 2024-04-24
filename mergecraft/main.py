import os
import tempfile
import subprocess
import fnmatch
from .file_utils import find_subdir, read_file_content
from .cli_parser import parse_arguments
from .constants import DEFAULT_EXTENSIONS
import re

def main():
    args = parse_arguments()

    # Normalização dos argumentos de linha de comando
    if args.path != "." and not args.extensions:
        args.extensions = [""]
    if not args.extensions:
        args.extensions = DEFAULT_EXTENSIONS

    # Validação do regex fornecido, se houver
    if args.filter:
        try:
            re.compile(args.filter)
        except re.error:
            print("Error: Invalid regular expression provided!")
            return

    # Obtenção e validação do caminho completo
    full_path = os.path.normpath(os.path.join(os.getcwd(), args.path))
    if not os.path.exists(full_path):
        full_path = find_subdir(os.getcwd(), args.path)
        if not full_path:
            print(f"Error: The specified path '{args.path}' was not found.")
            return

    # Criação de arquivo temporário para a concatenação dos conteúdos
    temp_path = tempfile.mktemp(prefix="mergecraft_", suffix=".txt")
    read_files, total_line_count = process_files(full_path, args, temp_path)

    # Abertura do arquivo temporário no VS Code
    edit_in_vscode(temp_path)

    # Resumo e limpeza
    print_summary(read_files, total_line_count)
    os.remove(temp_path)

def process_files(full_path, args, temp_path):
    read_files = []
    total_line_count = 0
    for dirpath, dirnames, filenames in os.walk(full_path):
        for filename in filenames:
            if not should_include_file(filename, args.extensions, dirpath):
                continue
            filepath = os.path.join(dirpath, filename)
            content = read_file_content(filepath)
            if args.filter and not matches_filter(content, filename, args.filter):
                continue
            line_count = write_to_temp_file(filepath, filename, content, temp_path)
            read_files.append((filepath, line_count))
            total_line_count += line_count
    return read_files, total_line_count

def should_include_file(filename, extensions, dirpath):
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            gitignore_content = f.read().splitlines()
        for pattern in gitignore_content:
            if pattern.startswith("#") or not pattern.strip():
                continue
            if pattern.startswith("/"):
                pattern = pattern[1:]
            if fnmatch.fnmatch(filename, pattern):
                return False
    return filename.endswith(tuple(extensions))

def matches_filter(content, filename, filter_regex):
    return re.search(filter_regex, content) or re.search(filter_regex, filename)

def write_to_temp_file(filepath, filename, content, temp_path):
    line_count = content.count('\n') + 1
    with open(temp_path, 'a', encoding='utf-8') as f:
        f.write(f"```{filename}\n{content}\n```\n\n")
    return line_count

def edit_in_vscode(temp_path):
    print("Editing in VS Code. Close to continue.")
    code_path = r'C:\Program Files\Microsoft VS Code\bin\code.exe'
    subprocess.run([code_path, '-w', temp_path])

def print_summary(read_files, total_line_count):
    if read_files:
        print("\nSummary:")
        print(f"Total files read: {len(read_files)}")
        print(f"Total lines: {total_line_count}")
        print("\nFiles read:")
        for file_path, line_count in read_files:
            print(f"{file_path}: {line_count} lines")
    else:
        print("No files were read!")

if __name__ == "__main__":
    main()
