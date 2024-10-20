import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text node")

    def test_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, "bold")
        
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="URL.com")
        self.assertEqual(node.url, "URL.com")
        
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, url="URL.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, URL.com)")

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="URL.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="DifferentURL.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()