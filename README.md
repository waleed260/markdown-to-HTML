# MD-Transpiler: Markdown to HTML Converter

A Python-based Markdown to HTML converter built from scratch without external libraries.

## Features

- **Header parsing**: Supports `# Header 1`, `## Header 2`, etc.
- **Text formatting**: Bold (`**text**`), italic (`*text*`), and bold-italic (`***text***`)
- **Unordered lists**: Supports nested lists with `- item`
- **Hyperlinks**: Parses `[text](url)` format
- **HTML5 output**: Generates valid HTML5 documents with proper structure
- **CSS injection**: Optional CSS file support for styling
- **Command-line interface**: Easy-to-use CLI with argument support

## Installation

```bash
pip install -e .
```

## Usage

Basic usage:
```bash
python -m src.md_converter.main input.md
```

With custom output file:
```bash
python -m src.md_converter.main input.md -o output.html
```

With CSS injection:
```bash
python -m src.md_converter.main input.md --css styles.css -o output.html
```

## Supported Markdown Syntax

### Headers
```markdown
# H1
## H2
### H3
#### H4
##### H5
###### H6
```

### Text Formatting
```markdown
**Bold text**
*Italic text*
***Bold and italic text***
```

### Lists
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3
```

### Links
```markdown
[Link text](https://example.com)
```

## Architecture

The converter is built with modularity in mind:

- `MarkdownParser`: Handles the parsing logic for different markdown elements
- `convert_md_to_html`: Wraps the parsed content in a complete HTML document
- `main`: Entry point with command-line argument parsing

All parsing is done using regular expressions and string manipulation, without relying on external markdown libraries.
