import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Merge files into a temporary file and open in VS Code.")
    parser.add_argument("-e", "--extensions", nargs="+", default=None, help="Specify the file extensions to process.")
    parser.add_argument("--path", default=".", help="Specify the root path to start searching for files. Defaults to current directory.")
    parser.add_argument("--filter", help="A regex pattern to filter files based on their content or name. Only files matching this pattern will be included.")
    return parser.parse_args()
