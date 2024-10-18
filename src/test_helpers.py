import unittest
from textnode import TextNode, TextType
from helpers import split_nodes_delimiter

# Mapping of TextType to their respective delimiters
delimiters = {
    TextType.BOLD: "**",
    TextType.ITALIC: "*",
    TextType.CODE: "`",
    TextType.LINK: ":",
    TextType.IMAGE: "!"
}

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_single_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_split_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_split_italic_text(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_split_link_text(self):
        node = TextNode("This is a :link: to somewhere", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK),
            TextNode(" to somewhere", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], ":", TextType.LINK)
        self.assertEqual(result, expected)

    def test_split_image_text(self):
        node = TextNode("This is an !image! in text", TextType.TEXT)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE),
            TextNode(" in text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "!", TextType.IMAGE)
        self.assertEqual(result, expected)

    def test_no_split(self):
        node = TextNode("This text has no delimiter", TextType.TEXT)
        expected = [node]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and *italic* text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()