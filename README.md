# mergecraft 🚀

[![Upload Python Package](https://github.com/josenerydev/mergecraft/actions/workflows/python-publish.yml/badge.svg)](https://github.com/josenerydev/mergecraft/actions/workflows/python-publish.yml)
![GitHub](https://img.shields.io/github/license/josenerydev/mergecraft)
![PyPI](https://img.shields.io/pypi/v/mergecraft)
![Python Version](https://img.shields.io/pypi/pyversions/mergecraft)

`mergecraft` is a command-line tool engineered to assist development teams by merging files into a single temporary file and then opening it in Visual Studio Code. This tool is particularly useful in AI-driven development environments, where understanding the broader context of code changes is crucial.

## 🌟 Introduction to AI-Driven Development with mergecraft

In AI-driven development, tools like `mergecraft` play a pivotal role by reducing the cognitive load on developers. It enables them to focus more on refining the technology rather than getting bogged down with mundane tasks. By merging related files into a single view, `mergecraft` helps in providing a consolidated context, enhancing the capabilities of AI code assistants like StackSpot AI.

### 🚀 Benefits of Using mergecraft

- **Enhanced Productivity**: Speeds up the development process by merging files quickly and efficiently, allowing developers to see everything in one place.
- **Reduced Errors**: Minimizes the chance of overlooking context-related errors by providing a unified view of multiple files.
- **Support for AI Code Assistants**: Improves the effectiveness of AI-driven tools which rely on understanding code in context, aiding in intelligent code completion and error correction.

## ⚙️ Installation

### Setting Up Your Environment

To set up the `mergecraft` tool, you can now install it directly from PyPI:

```bash
pip install mergecraft
```

### 📦 Install Locally

Alternatively, if you need to install from the source for the latest features or development purposes:

```bash
# Clone the repository
git clone https://github.com/your-username/mergecraft.git
cd mergecraft

# Create and activate a virtual environment
python -m venv env
source env/Scripts/activate  # Windows
source env/bin/activate      # Unix/Mac

# Install dependencies
pip install -r requirements.txt

# Install mergecraft
pip install .

# Deactivate the virtual environment
deactivate
```

## 🛠 How to Use mergecraft

Once installed, you can use `mergecraft` from any terminal:

```bash
mergecraft [options]
```

### 📝 Command-line Options

- `-e`, `--extensions`: Specify which file extensions to include in the merge. Defaults to settings in `mergecraft.config.yml`.
- `--path`: Set the root path for searching files. Defaults to the current directory.
- `--filter`: Apply a regex filter to select files based on content or name.

### ⚙️ Configuration via mergecraft.config.yml

Configure `mergecraft` by editing the `mergecraft.config.yml` file, which allows you to specify extensions, and files or directories to skip:

```yaml
extensions:
  - ".py"
  - ".txt"
skip_files:
  - ".gitignore"
  - "LICENSE"
  - "README.md"
  - "__init__.py"
  - "_*"
skip_directories:
  - "bin"
  - "obj"
  - ".git"
```

## 🎯 AI in Development: The Role of mergecraft

`mergecraft` supports AI-driven development by automating routine tasks like file merging, aiding in documentation, and streamlining code reviews. It helps bridge the gap between developers' needs for consistency and the requirements of fast-paced technology environments, making it an indispensable tool for modern development teams.

## 📜 License

`mergecraft` is released under the MIT License. See the LICENSE file for more details.
