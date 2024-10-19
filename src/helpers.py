from textnode import TextNode, TextType
from typing import List
import re

textType_mappings = {
    "text": TextType.TEXT,
    "bold": TextType.BOLD,
    "italic": TextType.ITALIC,
    "code": TextType.CODE,
    "link": TextType.LINK,
    "image": TextType.IMAGE
}

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Splits the text nodes based on a delimiter and creates new text nodes with alternating text types.

    This function takes a list of text nodes and a delimiter string and splits the text nodes based on the delimiter.
    It then creates new text nodes with alternating text types for each split text segment.

    Parameters:
    old_nodes ([TextNode]): A list of text nodes to be split.
    delimiter (str): The delimiter string used to split the text nodes.
    text_type (TextType): The text type for the segments between delimiters.

    Returns:
    [TextNode]: A list of new text nodes with alternating text types.

    Example:
    >>> node = TextNode("This is text with a `code block` word", TextType.TEXT)
    >>> new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    """
    new_nodes = []
    for node in old_nodes:
        # if re.search(r"\ +" + re.escape(delimiter) + r"+" + re.escape(delimiter) + r"\ +", node.text) is None:
        #     new_nodes.append(node)
        #     continue
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            current_text_type = textType_mappings[node.text_type] if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part, current_text_type, node.url if i % 2 == 0 else None))
    return new_nodes

def extract_markdown_images(text: str) -> List[tuple]:
    """
    Extracts all markdown image references from the given text.

    Args:
        text (str): The input text containing markdown image references.

    Returns:
        list of tuple: A list of tuples where each tuple contains the alt text and the URL of an image.

    Example:
    >>> text = "Here is an image ![alt text](http://example.com/image.jpg)"
    >>> extract_markdown_images(text)
    [('alt text', 'http://example.com/image.jpg')]
    """
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> List[tuple]:
    """
    Extracts all markdown link references from the given text.

    Args:
        text (str): The input text containing markdown link references.

    Returns:
        list of tuple: A list of tuples where each tuple contains the link text and the URL of a link.

    Example:
    >>> text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    >>> extract_markdown_links(text)
    [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    """
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Splits nodes containing markdown images into separate text and image nodes.

    Args:
        old_nodes (list): A list of nodes, where each node has a 'text' attribute 
        containing markdown content.

    Returns:
        list: A list of nodes where markdown images are split into separate 
        TextNode objects. TextNode objects have a type attribute indicating 
        whether they are text or image nodes.

    Example:
        Given a node with text "Here is an image ![alt text](url)", the function will 
        return three nodes: one with text "Here is an image ", one with the image alt text, 
        and one with text after the image.
    """
    nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        prev_end = 0
        if len(images) == 0:
            nodes.append(node)
        else:
            matches = re.finditer(r"!\[.*?\]\(.*?\)", node.text)
            for i, match in enumerate(matches):
                start, end = match.span()
                if start > 0:
                    nodes.append(TextNode(node.text[prev_end:start], TextType.TEXT))
                nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                prev_end = end
            if prev_end < len(node.text):
                nodes.append(TextNode(node.text[prev_end:], TextType.TEXT))
    return nodes

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Splits nodes containing markdown links into separate text and link nodes.

    Args:
        old_nodes (list): A list of nodes, where each node has a 'text' attribute 
        containing markdown content.

    Returns:
        list: A list of nodes where markdown links are split into separate 
        TextNode objects. TextNode objects have a type attribute indicating 
        whether they are text or link nodes.

    Example:
        Given a node with text "This is a [link](url)", the function will 
        return three nodes: one with text "This is a ", one with the link text, 
        and one with text after the link.
    """
    nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        prev_end = 0
        if len(links) == 0:
            nodes.append(node)
        else:
            matches = re.finditer(r"\[.*?\]\(.*?\)", node.text)
            for i, match in enumerate(matches):
                start, end = match.span()
                if start > 0:
                    nodes.append(TextNode(node.text[prev_end:start], TextType.TEXT))
                nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                prev_end = end
            if prev_end < len(node.text):
                nodes.append(TextNode(node.text[prev_end:], TextType.TEXT))
    return nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    """
    Converts a text string into a list of TextNode objects, splitting the text
    based on various markdown delimiters and creating nodes with appropriate
    text types.

    Args:
        text (str): The input text containing markdown content.

    Returns:
        List[TextNode]: A list of TextNode objects with appropriate text types.

    Example:
        >>> text = "This is **bold** and `code` and *italic* text with ![alt](image.png) and [link](url)"
        >>> nodes = text_to_textnodes(text)
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
    """
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes