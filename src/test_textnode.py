import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_eq_text(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text, "This is a text node")

    def test_type(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text_type, "bold")
        
    def test_url(self):
        node = TextNode("This is a text node", "bold", "URL.com")
        self.assertEqual(node.url, "URL.com")
        
    def test_url_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()