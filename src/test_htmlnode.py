import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        # Test initialization of HTMLNode with all parameters
        node = HTMLNode("div", "content", [], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_init_defaults(self):
        # Test initialization of HTMLNode with default parameters
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_empty(self):
        # Test props_to_html method with no properties
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        # Test props_to_html method with properties
        node = HTMLNode(props={"class": "container", "id": "my-div"})
        self.assertEqual(node.props_to_html(), ' class="container" id="my-div"')

    def test_eq(self):
        # Test equality of two identical HTMLNode instances
        node1 = HTMLNode("div", "content", [], {"class": "container"})
        node2 = HTMLNode("div", "content", [], {"class": "container"})
        self.assertEqual(node1, node2)

    def test_eq_different_tag(self):
        # Test inequality of HTMLNode instances with different tags
        node1 = HTMLNode("div", "content")
        node2 = HTMLNode("span", "content")
        self.assertNotEqual(node1, node2)

    def test_eq_different_value(self):
        # Test inequality of HTMLNode instances with different values
        node1 = HTMLNode("div", "content1")
        node2 = HTMLNode("div", "content2")
        self.assertNotEqual(node1, node2)

    def test_eq_different_children(self):
        # Test inequality of HTMLNode instances with different children
        node1 = HTMLNode("div", "content", [HTMLNode("span")])
        node2 = HTMLNode("div", "content", [HTMLNode("p")])
        self.assertNotEqual(node1, node2)

    def test_eq_different_props(self):
        # Test inequality of HTMLNode instances with different properties
        node1 = HTMLNode("div", "content", props={"class": "container"})
        node2 = HTMLNode("div", "content", props={"class": "row"})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        # Test string representation of HTMLNode
        node = HTMLNode("div", "content", [], {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, content, [], {'class': 'container'})")

class TestLeafNode(unittest.TestCase):

    def test_init(self):
        # Test initialization of LeafNode with all parameters
        node = LeafNode("span", "content", {"class": "text"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "text"})

    def test_to_html_with_tag_and_props(self):
        # Test to_html method with tag and properties
        node = LeafNode("span", "content", {"class": "text"})
        self.assertEqual(node.to_html(), '<span class="text">content</span>')

    def test_to_html_with_tag_and_props_href(self):
        # Test to_html method with tag and href property
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_tag_no_props(self):
        # Test to_html method with tag and no properties
        node = LeafNode("p", "paragraph")
        self.assertEqual(node.to_html(), "<p>paragraph</p>")

    def test_to_html_no_tag(self):
        # Test to_html method with no tag
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_empty_tag(self):
        # Test to_html method with empty tag
        node = LeafNode("", "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_no_value_raises_error(self):
        # Test to_html method raises error when value is None
        node = LeafNode("span", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All leaf nodes must have a value."
        )

class TestParentNode(unittest.TestCase):

    def test_init(self):
        # Test initialization of ParentNode with children
        children = [
            LeafNode("p", "First child"),
            LeafNode("p", "First child")
        ]
        node = ParentNode("div", children)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, None)

    def test_to_html_basic(self):
        # Test to_html method with basic structure
        node = ParentNode("p", [LeafNode("li", "Item 1"),LeafNode("li", "Item 2")])
        val = node.to_html()
        self.assertEqual(val, "<p><li>Item 1</li><li>Item 2</li></p>")

    def test_to_html_multi_leaf(self):
        # Test to_html method with multiple leaf nodes
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("p", children)
        val = node.to_html()
        self.assertEqual(val, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_to_html_no_tag(self):
        # Test to_html method raises error when tag is None
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(None, children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All parent nodes must have a tag."
        )
    
    def test_to_html_empty_tag(self):
        # Test to_html method raises error when tag is empty
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("", children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All parent nodes must have a tag."
        )
    
    def test_to_html_no_children_list(self):
        # Test to_html method raises error when children is not a list
        children = "None"
        node = ParentNode("p", children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All parent nodes must have a children list."
        )
    
    def test_to_html_no_children(self):
        # Test to_html method raises error when children is None
        children = None
        node = ParentNode("p", children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All parent nodes must have a children list."
        )
    
    def test_to_html_empty_children(self):
        # Test to_html method raises error when children list is empty
        children = []
        node = ParentNode("p", children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All parent nodes must have a children list."
        )
    
    def test_to_html_nested_parent(self):
        # Test to_html method with nested parent nodes
        inner_children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        outer_children = [ParentNode("ul", inner_children)]
        node = ParentNode("p", outer_children)
        val = node.to_html()
        self.assertEqual(val, "<p><ul><b>Bold text</b>Normal text<i>italic text</i>Normal text</ul></p>")

    def test_to_html_with_props(self):
        # Test to_html method with properties
        children = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2")
        ]
        node = ParentNode("ul", children, {"class": "list"})
        val = node.to_html()
        self.assertEqual(val, '<ul class="list"><li>Item 1</li><li>Item 2</li></ul>')

    def test_to_html_with_empty_children(self):
        # Test to_html method with empty children list
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception), 
            "All parent nodes must have a children list."
        )

if __name__ == '__main__':
    unittest.main()