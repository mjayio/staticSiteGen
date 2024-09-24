import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is a text node", "bold")
        node2 = HTMLNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_eq_text(self):
        node = HTMLNode("This is a text node", "bold")
        self.assertEqual(node.tag, "This is a text node")

    def test_type(self):
        node = HTMLNode("This is a text node", "bold")
        self.assertEqual(node.value, "bold")
        
    def test_url(self):
        node = HTMLNode("This is a text node", "bold", "URL.com")
        self.assertEqual(node.children, "URL.com")
        
    def test_url_none(self):
        node = HTMLNode("This is a text node", "bold")
        self.assertEqual(node.props, None)


if __name__ == "__main__":
    unittest.main()