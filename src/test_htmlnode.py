import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        node = HTMLNode("div", "content", [], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_init_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "container", "id": "my-div"})
        self.assertEqual(node.props_to_html(), ' class="container" id="my-div"')

    def test_eq(self):
        node1 = HTMLNode("div", "content", [], {"class": "container"})
        node2 = HTMLNode("div", "content", [], {"class": "container"})
        self.assertEqual(node1, node2)

    def test_eq_different_tag(self):
        node1 = HTMLNode("div", "content")
        node2 = HTMLNode("span", "content")
        self.assertNotEqual(node1, node2)

    def test_eq_different_value(self):
        node1 = HTMLNode("div", "content1")
        node2 = HTMLNode("div", "content2")
        self.assertNotEqual(node1, node2)

    def test_eq_different_children(self):
        node1 = HTMLNode("div", "content", [HTMLNode("span")])
        node2 = HTMLNode("div", "content", [HTMLNode("p")])
        self.assertNotEqual(node1, node2)

    def test_eq_different_props(self):
        node1 = HTMLNode("div", "content", props={"class": "container"})
        node2 = HTMLNode("div", "content", props={"class": "row"})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = HTMLNode("div", "content", [], {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, content, [], {'class': 'container'})")

class TestLeafNode(unittest.TestCase):

    def test_init(self):
        node = LeafNode("span", "content", {"class": "text"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "text"})

    def test_to_html_with_tag_and_props(self):
        node = LeafNode("span", "content", {"class": "text"})
        self.assertEqual(node.to_html(), '<span class="text">content</span>')

    def test_to_html_with_tag_and_props_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_tag_no_props(self):
        node = LeafNode("p", "paragraph")
        self.assertEqual(node.to_html(), "<p>paragraph</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_empty_tag(self):
        node = LeafNode("", "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_no_value_raises_error(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All leaf nodes must have a value."
        )

if __name__ == '__main__':
    unittest.main()