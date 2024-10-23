import os
import re
import shutil
from blocks_helper import markdown_to_html_node


def main():
    delete_public_dir()
    copy_src_dir_to_dest_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def copy_src_dir_to_dest_dir(src_dir: str, dest_dir: str) -> None:
    """
    Copies the contents of the source directory to the destination directory.
    This function performs the following steps:
    1. Determines the current project location.
    2. Deletes the contents of the destination directory if it exists.
    3. Creates the destination directory.
    4. Checks if the source directory exists.
    5. Copies the source directory to the destination directory with detailed logging.
    
    Args:
        src_dir (str): The relative path to the source directory from the project root.
        dest_dir (str): The relative path to the destination directory from the project root.
    
    Returns:
        None
    """
    # Get the current project location
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Go back one directory to get the root directory
    curr_proj_loc = os.path.dirname(curr_dir)
    
    # Delete contents of dest_dir if it exists
    full_dest_dir = os.path.join(curr_proj_loc, dest_dir)
    if os.path.exists(full_dest_dir):
        shutil.rmtree(full_dest_dir)
        print(f"Deleted existing directory: {full_dest_dir}")
    
    # Create dest_dir
    os.makedirs(full_dest_dir, exist_ok=True)
    print(f"Created directory: {full_dest_dir}")

    full_src_dir = os.path.join(curr_proj_loc, src_dir)
    
    # Check if src_dir exists
    if not os.path.exists(full_src_dir):
        print(f"Source directory {src_dir} does not exist")
        return
    
    # Copy src_dir to dest_dir with detailed logging
    shutil.copytree(full_src_dir, full_dest_dir, dirs_exist_ok=True)
    print(f"Successfully copied {src_dir} to {dest_dir}")


def extract_title(markdown: str) -> str:
    """
    Extracts the title from a markdown string.

    This function searches for the first level-1 header (H1) in the provided markdown text.
    It assumes that the title is the first line that starts with a single '#' followed by a space.
    If no such line is found, it raises an exception.

    Args:
        markdown (str): The markdown content as a string.

    Returns:
        str: The title extracted from the markdown content.

    Raises:
        ValueError: If no level-1 header is found in the markdown content.
    """
    # Find all lines that start with a single '#' followed by a space
    h1_header_lines = re.findall(r"^# (.+)", markdown, re.MULTILINE)
    
    # If no such lines are found, raise an exception
    if not h1_header_lines:
        raise ValueError("No title found in markdown")
    
    # Return the first matching line
    return h1_header_lines[0]


def delete_public_dir():
    """
    Deletes the 'public' directory if it exists.

    This function checks if a directory named 'public' exists in the current working directory.
    If it does, the directory and all its contents are removed. A message is printed to the console
    indicating that the 'public' directory has been deleted.

    Raises:
        OSError: If the directory cannot be removed due to permission issues or if it is in use.
    """
    public_dir = os.path.join(os.getcwd(), "public")
    
    # Check if the 'public' directory exists
    if os.path.exists(public_dir):
        try:
            # Remove the 'public' directory and all its contents
            shutil.rmtree(public_dir)
            # Print a message indicating that the 'public' directory has been deleted
            print(f"Deleted public directory: {public_dir}")
        except OSError as e:
            print(f"Error: {public_dir} : {e.strerror}")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Generates an HTML page from a markdown file using a specified template.

    Args:
        from_path (str): The file path to the markdown source file.
        template_path (str): The file path to the HTML template file.
        dest_path (str): The destination file path where the generated HTML page will be saved.

    Raises:
        IOError: If there is an issue reading from the source or template files, or writing to the destination file.

    Notes:
        - The function reads the markdown content from `from_path`, converts it to HTML, and extracts the title.
        - The HTML content and title are then inserted into the template specified by `template_path`.
        - The final HTML content is written to the file specified by `dest_path`.
        - If the directory for `dest_path` does not exist, it will be created.
    """
    # Print a message indicating the start of the page generation process
    print(f"Generating page from {from_path} using {template_path} to {dest_path}")
    
    # Read the markdown content from the source file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the HTML template content from the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert the markdown content to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()
    
    # Extract the title from the markdown content
    title = extract_title(markdown_content)
    
    # Replace the placeholder for the title in the template with the actual title
    template_content = template_content.replace("{{ Title }}", title)
    
    # Replace the placeholder for the content in the template with the generated HTML content
    template_content = template_content.replace("{{ Content }}", html_content)
    
    # Ensure the destination directory exists, create it if it does not
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML content to the destination file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
    Recursively generates HTML pages from markdown files in a specified content directory.
    This function traverses the given content directory, processes each markdown file found,
    and generates corresponding HTML files using a specified template. The generated HTML files
    are saved in the destination directory, preserving the relative directory structure.
    Args:
        dir_path_content (str): The path to the directory containing markdown content files.
        template_path (str): The path to the HTML template file used for generating pages.
        dest_dir_path (str): The path to the destination directory where generated HTML files will be saved.
    Raises:
        FileNotFoundError: If the content directory or the template file does not exist.
        IOError: If an error occurs during the generation of an HTML page.
    Example:
        generate_pages_recursive('/path/to/content', '/path/to/template.html', '/path/to/destination')
    Note:
        - The function assumes that the `generate_page` function is defined elsewhere in the codebase.
        - The destination directory structure will mirror the content directory structure, with markdown
          files converted to HTML files.
    """
    # Check if the content directory exists
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Content directory {dir_path_content} does not exist")

    # Check if the template file exists
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template file {template_path} does not exist")

    # Recursively generate pages from markdown files in dir_path_content
    for dirpath, _, filenames in os.walk(dir_path_content):
        for filename in filenames:
            # Check if the file is a markdown file
            if filename.endswith(".md"):
                # Construct the full path to the markdown file
                page_path = os.path.join(dirpath, filename)
                
                # Determine the destination path for the generated HTML file
                relative_path = os.path.relpath(page_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")
                
                # Generate the HTML page from the markdown file using the template
                try:
                    generate_page(page_path, template_path, dest_path)
                    print(f"Generated HTML for {page_path} at {dest_path}")
                except IOError as e:
                    print(f"Error generating page for {page_path}: {e}")


if __name__ == "__main__":
    main()
