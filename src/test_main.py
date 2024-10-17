import unittest
from main import text_node_to_html_node
from textnode import TextNode, NodeType
from htmlnode import LeafNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node(self):
        text_node = TextNode("Hello, World!", NodeType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("", "Hello, World!"))

    def test_bold_node(self):
        text_node = TextNode("Hello, World!", NodeType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("b", "Hello, World!"))

    def test_italic_node(self):
        text_node = TextNode("Hello, World!", NodeType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("i", "Hello, World!"))

    def test_code_node(self):
        text_node = TextNode("print('Hello, World!')", NodeType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("code", "print('Hello, World!')"))

    def test_link_node(self):
        text_node = TextNode("Click here", NodeType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("a", "Click here", {"href": "https://example.com"}))

    def test_image_node(self):
        text_node = TextNode("Image description", NodeType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("img", "", {"src": "https://example.com/image.png", "alt": "Image description"}))

    def test_empty_text_node(self):
        text_node = TextNode("", NodeType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("", ""))

    def test_empty_bold_node(self):
        text_node = TextNode("", NodeType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("b", ""))

    def test_empty_italic_node(self):
        text_node = TextNode("", NodeType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("i", ""))

    def test_empty_code_node(self):
        text_node = TextNode("", NodeType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("code", ""))

    def test_empty_link_node(self):
        text_node = TextNode("", NodeType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("a", "", {"href": "https://example.com"}))

    def test_empty_image_node(self):
        text_node = TextNode("", NodeType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("img", "", {"src": "https://example.com/image.png", "alt": ""}))

if __name__ == "__main__":
    unittest.main()