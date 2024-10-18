from textnode import TextType, TextNode
from htmlnode import LeafNode

def main():
    textnode = TextNode("hello world", TextType.TEXT, "https://example.com")
    print(text_node_to_html_node(textnode))

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Converts a text node to an HTML node.

    This function takes a text node object and converts it into an HTML node
    based on the type of the text node. The conversion is done using a match-case
    statement that checks the `text_type` attribute of the text node and returns
    an appropriate `LeafNode` object.

    Parameters:
    text_node (TextNode): The text node object to be converted. It must have the
                          following attributes:
                          - text_type (str): The type of the text node. It can be
                            one of the following values: "text", "bold", "italic",
                            "code", "link", "image".
                          - text (str): The text content of the node.
                          - url (str, optional): The URL for link or image nodes.

    Returns:
    LeafNode: An HTML node represented as a `LeafNode` object. The tag and attributes
              of the `LeafNode` depend on the `text_type` of the input `text_node`.

    Raises:
    ValueError: If the `text_type` of the text node is not one of the expected values.

    Example:
    >>> text_node = TextNode(text="Hello, World!", text_type="bold")
    >>> html_node = text_node_to_html_node(text_node)
    >>> print(html_node)
    LeafNode(tag="b", text="Hello, World!")
    """
    match text_node.text_type:
        case "text":
            return LeafNode("", text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

if __name__ == "__main__":
    main()
