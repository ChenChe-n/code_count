[English](README.md) | [中文](README_zh.md)

# Code Line Counter

A powerful code line counting tool that supports multiple programming languages with high performance, accurate comment recognition, and cross-platform capabilities.

## Features

- 🚀 **High Performance**: Utilizes multithreading to process files in parallel, greatly improving counting speed
- 🌍 **Multi-language Support**: Supports 30+ programming language including Python, Java, JavaScript, C++, HTML, CSS, etc.
- 💬 **Smart Comment Recognition**: Accurately distinguishes between code lines, comment lines, and empty lines
- 🔤 **Character Counting**: Counts code characters and comment characters
- 📊 **Visual Output**: Uses Rich library to provide beautiful tabular output
- 🌐 **Internationalization**: Supports both Chinese and English interfaces with automatic switching
- 🧠 **Intelligent Encoding Detection**: Automatically detects file encoding, supporting UTF-8, GBK and other encodings
- 🗂️ **File Mode**: Optional file mode for real-time output of statistics for each file
- ⏱️ **Progress Display**: Shows real-time processing progress
- 🚫 **Ignore Rules**: Automatically ignores common development tool directories like `.git`, `node_modules`, etc.

## Supported Languages

- Python (.py)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- HTML (.html, .htm)
- CSS (.css)
- JSON (.json)
- XML (.xml)
- YAML (.yml, .yaml)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Shell (.sh)
- PowerShell (.ps1)
- Lua (.lua)
- Markdown (.md)
- CMake (.cmake, CMakeLists.txt)
- And more...

## Requirements

- Python 3.6+
- Dependencies:
  - `rich` >= 10.0.0
  - `chardet` >= 4.0.0

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install separately:
   ```bash
   pip install rich>=10.0.0
   pip install chardet>=4.0.0
   ```

## Usage

### Basic Usage

```bash
python main.py
```

This will count all code files in the current directory.

### Specify Paths

```bash
python main.py /path/to/code
python main.py /path/to/project1 /path/to/project2
```

### File Mode

Use the `-f` or `--file-mode` parameter to enable file mode, which outputs detailed information immediately after processing each file:

```bash
python main.py -f
python main.py --file-mode /path/to/code
```

### Paths with Spaces

If the path contains spaces, please surround it with quotes:

```bash
python main.py "/path/to/my project"
```

## Output Explanation

The tool outputs a table containing the following columns:

- **Language**: Programming language type of the files
- **Files**: Number of files of that language type
- **Code Lines**: Actual lines of code (excluding comments and empty lines)
- **Comment Lines**: Number of comment lines
- **Empty Lines**: Number of empty lines
- **Code Chars**: Non-whitespace characters in code lines
- **Comment Chars**: Non-whitespace characters in comment lines

## License

MIT License