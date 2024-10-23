from enum import Enum
import re
from typing import List
from htmlnode import HTMLNode, ParentNode
from inline_helpers import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    HEADING4 = "heading4"
    HEADING5 = "heading5"
    HEADING6 = "heading6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Converts a markdown string into a list of text blocks.
    This function processes the input markdown string by compressing multiple
    consecutive blank lines into a single blank line, then splitting the string
    into blocks based on double newlines. Each block is then stripped of leading
    and trailing whitespace and newlines.
    Args:
        markdown (str): The markdown string to be converted into blocks.
    Returns:
        List[str]: A list of text blocks derived from the input markdown.
    """
    # Compress two or more blank lines into just one blank line
    markdown = re.sub(r"\n{2,}", "\n\n", markdown)
    
    # Split the markdown into blocks based on double newlines
    blocks_unstripped = markdown.split("\n\n")
    
    # Strip leading and trailing whitespace and newlines from each block
    blocks_stripped = [block.strip(" \n") for block in blocks_unstripped]
    
    return blocks_stripped


def block_to_block_type(markdown_block: str) -> BlockType:
    """
    Determines the type of a given markdown block.

    Args:
        markdown_block (str): A string representing a block of markdown text.

    Returns:
        BlockType: An enumeration value representing the type of the markdown block.

    BlockType can be one of the following:
        - BlockType.HEADING1: If the block is a markdown heading (starts with 1 hash symbol followed by a space).
        - BlockType.HEADING2: If the block is a markdown heading (starts with 2 hash symbols followed by a space).
        - BlockType.HEADING3: If the block is a markdown heading (starts with 3 hash symbols followed by a space).
        - BlockType.HEADING4: If the block is a markdown heading (starts with 4 hash symbols followed by a space).
        - BlockType.HEADING5: If the block is a markdown heading (starts with 5 hash symbols followed by a space).
        - BlockType.HEADING6: If the block is a markdown heading (starts with 6 hash symbols followed by a space).
        - BlockType.CODE: If the block is a code block (enclosed by triple backticks).
        - BlockType.QUOTE: If the block is a blockquote (starts with a greater-than symbol).
        - BlockType.UNORDERED_LIST: If the block is an unordered list item (starts with asterisk or hyphen followed by a space).
        - BlockType.ORDERED_LIST: If the block is an ordered list item (starts with a number followed by a period and a space).
        - BlockType.PARAGRAPH: If the block does not match any of the above types, it is considered a paragraph.
    """
    if re.search(r"^#{1} ", markdown_block):
        return BlockType.HEADING1
    if re.search(r"^#{2} ", markdown_block):
        return BlockType.HEADING2
    if re.search(r"^#{3} ", markdown_block):
        return BlockType.HEADING3
    if re.search(r"^#{4} ", markdown_block):
        return BlockType.HEADING4
    if re.search(r"^#{5} ", markdown_block):
        return BlockType.HEADING5
    if re.search(r"^#{6} ", markdown_block):
        return BlockType.HEADING6
    if re.search(r"^```", markdown_block) and re.search(r"```$", markdown_block):
        return BlockType.CODE
    if re.search(r"^>", markdown_block):
        return BlockType.QUOTE
    if re.search(r"^[*-] ", markdown_block):
        return BlockType.UNORDERED_LIST
    if re.search(r"^\d+\. ", markdown_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a markdown string into an HTMLNode tree structure.
    This function processes a markdown string, converts it into blocks, and then
    transforms each block into an appropriate HTML node. The resulting HTML nodes
    are then nested within a parent "div" node.
    Args:
        markdown (str): The markdown string to be converted.
    Returns:
        HTMLNode: A tree structure representing the HTML equivalent of the markdown input.
    The function performs the following steps:
    1. Converts the markdown string into blocks using `markdown_to_blocks`.
    2. Determines the type of each block using `block_to_block_type`.
    3. Converts each block into an HTML node based on its type.
    4. Processes the text within each block node to convert it into text nodes.
    5. Converts text nodes into HTML nodes and nests them appropriately.
    6. Wraps all block nodes within a parent "div" node and returns it.
    Block types handled:
    - HEADING1 to HEADING6: Converted to <h1> to <h6> tags.
    - CODE: Converted to <code> tag.
    - QUOTE: Converted to <blockquote> tag.
    - UNORDERED_LIST: Converted to <ul> tag.
    - ORDERED_LIST: Converted to <ol> tag.
    - Default: Converted to <p> tag.
    Example:
        markdown = "# Heading 1\n\nSome text."
        html_node = markdown_to_html_node(markdown)
        # html_node will represent the HTML structure:
        # <div>
        #   <h1>Heading 1</h1>
        #   <p>Some text.</p>
        # </div>
    """
    blocks = markdown_to_blocks(markdown)
    
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING1:
            block_nodes.append(HTMLNode("h1", block[2:]))
        elif block_type == BlockType.HEADING2:
            block_nodes.append(HTMLNode("h2", block[3:]))
        elif block_type == BlockType.HEADING3:
            block_nodes.append(HTMLNode("h3", block[4:]))
        elif block_type == BlockType.HEADING4:
            block_nodes.append(HTMLNode("h4", block[5:]))
        elif block_type == BlockType.HEADING5:
            block_nodes.append(HTMLNode("h5", block[6:]))
        elif block_type == BlockType.HEADING6:
            block_nodes.append(HTMLNode("h6", block[7:]))
        elif block_type == BlockType.CODE:
            block_nodes.append(HTMLNode("code", block[3:-3]))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(HTMLNode("blockquote", block[2:]))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(HTMLNode("ul", block))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(HTMLNode("ol", block))
        else:
            block_nodes.append(HTMLNode("p", block))
    
    new_block_nodes = []
    for block_node in block_nodes:
        text_nodes = []
        for text in block_node.value.split("\n"):
            text_nodes.extend(text_to_textnodes(text))
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        new_block_nodes.append(ParentNode(block_node.tag, html_nodes))
    
    html_node = ParentNode("div", new_block_nodes)
    return html_node
