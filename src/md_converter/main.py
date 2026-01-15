#!/usr/bin/env python3
"""
Markdown to HTML Converter
A Python-based Markdown transpiler built from scratch without external libraries.
"""

import re
import argparse
import os
import sys


class MarkdownParser:
    """A class to handle the parsing of markdown text to HTML."""

    def __init__(self):
        self.current_list_level = 0
        self.list_stack = []  # Track whether we're inside a list at each level

    def parse_headers(self, line):
        """Parse markdown headers (# Header 1, ## Header 2, etc.)"""
        # Match headers: # Header 1, ## Header 2, etc.
        header_pattern = r'^(#{1,6})\s+(.*)'
        match = re.match(header_pattern, line)

        if match:
            level = len(match.group(1))  # Number of # symbols
            content = self.parse_inline_elements(match.group(2))
            return f'<h{level}>{content}</h{level}>'
        return None

    def parse_unordered_lists(self, line):
        """Parse markdown unordered lists (- item)"""
        list_pattern = r'^(\s*)-\s+(.*)'
        match = re.match(list_pattern, line)

        if match:
            indent_spaces = len(match.group(1))
            indent_level = indent_spaces // 2  # 2 spaces per indent level

            content = self.parse_inline_elements(match.group(2))

            # Ensure the stack is the right size
            while len(self.list_stack) <= indent_level:
                self.list_stack.append(False)

            # Close any higher-level lists if we're reducing indentation
            closing_tags = ""
            for i in range(len(self.list_stack) - 1, indent_level, -1):
                if i < len(self.list_stack) and self.list_stack[i]:
                    closing_tags += "</ul>"
                    self.list_stack[i] = False

            # Generate appropriate opening tags if needed
            opening_tags = ""
            if not self.list_stack[indent_level]:
                # Need to open a list at this level
                opening_tags += "<ul>"
                self.list_stack[indent_level] = True

            # Clear any deeper levels that might have been left open
            for i in range(indent_level + 1, len(self.list_stack)):
                if i < len(self.list_stack) and self.list_stack[i]:
                    closing_tags += "</ul>"
                    self.list_stack[i] = False

            return f'{opening_tags}{closing_tags}<li>{content}</li>'
        return None

    def parse_inline_elements(self, text):
        """Parse inline markdown elements like bold, italic, and links"""
        # Parse links first: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        text = re.sub(link_pattern, r'<a href="\2">\1</a>', text)

        # Parse bold: **text** or __text__
        bold_pattern = r'\*\*(.*?)\*\*|__(.*?)__'
        text = re.sub(bold_pattern, r'<strong>\1\2</strong>', text)

        # Parse italic: *text* or _text_
        italic_pattern = r'(?<![*_])\*([^*]+)\*(?![*])|(?<![_])_([^_]+)_(?!_)'
        text = re.sub(italic_pattern, r'<em>\1\2</em>', text)

        # Handle bold and italic combinations: ***text*** or ___text___
        bold_italic_pattern = r'\*\*\*(.*?)\*\*\*|___(.*?)___'
        text = re.sub(bold_italic_pattern, r'<em><strong>\1\2</strong></em>', text)

        return text

    def parse_line(self, line):
        """Parse a single line of markdown"""
        # Check if it's a list item
        is_list_item = bool(re.match(r'^(\s*)-\s+', line))

        # If current line is not a list but we were in a list, close all open lists
        if not is_list_item:
            closing_tags = ""
            for i in range(len(self.list_stack) - 1, -1, -1):
                if self.list_stack[i]:
                    closing_tags += "</ul>"
                    self.list_stack[i] = False
            if closing_tags:
                # Reset list level
                self.current_list_level = 0
                # If we were expecting to output a header or paragraph, append it after closing tags
                header_result = self.parse_headers(line)
                if header_result:
                    return f'{closing_tags}{header_result}'

                if not line.strip():
                    return closing_tags

                content = self.parse_inline_elements(line.strip())
                return f'{closing_tags}<p>{content}</p>'

        # Try to parse as header
        header_result = self.parse_headers(line)
        if header_result:
            return header_result

        # Try to parse as list item
        list_result = self.parse_unordered_lists(line)
        if list_result:
            return list_result

        # If it's a blank line, return empty string
        if not line.strip():
            return ''

        # Otherwise, treat as paragraph
        content = self.parse_inline_elements(line.strip())
        return f'<p>{content}</p>'

    def parse(self, markdown_text):
        """Parse the entire markdown text"""
        lines = markdown_text.split('\n')
        html_lines = []

        for line in lines:
            parsed_line = self.parse_line(line)
            if parsed_line:
                html_lines.append(parsed_line)

        # Close any remaining open lists at the end of the document
        closing_tags = ""
        for i in range(len(self.list_stack) - 1, -1, -1):
            if self.list_stack[i]:
                closing_tags += "</ul>"
                self.list_stack[i] = False
        if closing_tags:
            html_lines.append(closing_tags)

        return '\n'.join(html_lines)


def convert_md_to_html(markdown_content, css_file=None):
    """
    Convert markdown content to a complete HTML document.

    Args:
        markdown_content (str): The markdown content to convert
        css_file (str, optional): Path to CSS file to inject

    Returns:
        str: Complete HTML document
    """
    parser = MarkdownParser()
    body_content = parser.parse(markdown_content)

    # Read CSS content if provided
    css_content = ""
    if css_file and os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()

    # Build the complete HTML document
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Document</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            margin-left: 20px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        {css_content}
    </style>
</head>
<body>
{body_content}
</body>
</html>"""

    return html_doc


def main():
    """Main function to handle command line arguments and process files"""
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML')
    parser.add_argument('input_file', nargs='?', default='document.md',
                        help='Input markdown file (default: document.md)')
    parser.add_argument('-o', '--output', default='index.html',
                        help='Output HTML file (default: index.html)')
    parser.add_argument('--css', help='CSS file to inject into the HTML')

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)

    try:
        # Read the markdown file
        with open(args.input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert to HTML
        html_content = convert_md_to_html(markdown_content, args.css)

        # Write the HTML output
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Successfully converted '{args.input_file}' to '{args.output}'")

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()