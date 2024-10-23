import os
import re
import shutil
from blocks_helper import markdown_to_html_node


def main():
    delete_public_dir()
    copy_src_dir_to_dest_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def copy_src_dir_to_dest_dir(src_dir, dest_dir):
    # get the current project location
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    
    # go back one directory to get the root directory
    curr_proj_loc = os.path.dirname(curr_dir)
    
    # delete contents of dest_dir if it exists
    full_dest_dir = os.path.join(curr_proj_loc, dest_dir)
    if os.path.exists(full_dest_dir):
        shutil.rmtree(full_dest_dir)
    
    # create dest_dir
    os.makedirs(full_dest_dir, exist_ok=True)

    full_src_dir = os.path.join(curr_proj_loc, src_dir)
    
    # check if src_dir exists
    if not os.path.exists(full_src_dir):
        print(f"{src_dir} does not exist")
        return
    
    # copy src_dir to dest_dir with detailed logging
    shutil.copytree(full_src_dir, full_dest_dir, dirs_exist_ok=True)
    print(f"Successfully copied {src_dir} to {dest_dir}")


def extract_title(markdown):
    h1_header_lines = re.findall(r"^# .+", markdown, re.MULTILINE)
    if not h1_header_lines:
        raise Exception("No title found in markdown")
    return h1_header_lines[0][2:]


def delete_public_dir():
    if os.path.exists("public"):
        shutil.rmtree("public")
        print("Deleted public directory")


def generate_page(from_path, template_path, dest_path):
    print("Generating page from", from_path, "using", template_path, "to", dest_path)
    data_from_path_file = open(from_path).read()
    data_template_path_file = open(template_path).read()
    html = markdown_to_html_node(data_from_path_file).to_html()
    title = extract_title(data_from_path_file)
    data_template_path_file = data_template_path_file.replace("{{ Title }}", title)
    data_template_path_file = data_template_path_file.replace("{{ Content }}", html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    dest_path_file = open(dest_path, "w")
    dest_path_file.write(data_template_path_file)
    dest_path_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # recursively generate pages from markdown files in dir_path_content
    for dirpath, dirnames, filenames in os.walk(dir_path_content):
        for filename in filenames:
            if filename.endswith(".md"):
                page_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(dest_dir_path, os.path.relpath(page_path, dir_path_content).replace(".md", ".html"))
                generate_page(page_path, template_path, dest_path)


if __name__ == "__main__":
    main()
