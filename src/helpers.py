from textnode import TextNode, TextType
from typing import List

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
    >>> nodes = [TextNode("Hello, World!", TextType.TEXT)]
    >>> split_nodes_delimiter(nodes, ",", TextType.BOLD)
    [TextNode("Hello", TextType.TEXT), TextNode(" World!", TextType.BOLD)]
    """
    new_nodes = []
    for node in old_nodes:
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            current_text_type = textType_mappings[node.text_type] if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part, current_text_type, node.url if i % 2 == 0 else None))
    return new_nodes