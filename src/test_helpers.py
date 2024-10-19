import unittest
from textnode import TextNode, TextType
from helpers import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

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


class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_single_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected, "Single image extraction failed result was " + str(result) + " expected was " + str(expected))
    
    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = "This is text with no images"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_image_with_no_alt_text(self):
        text = "This is text with an image ![](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("", "https://i.imgur.com/aKaOqIh.gif")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_image_with_special_characters_in_alt_text(self):
        text = "This is text with an image ![alt text with special characters !@#$%^&*()](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("alt text with special characters !@#$%^&*()", "https://i.imgur.com/aKaOqIh.gif")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_image_with_spaces_in_url(self):
        text = "This is text with an image ![alt text](https://i.imgur.com/aKaOqIh%20with%20spaces.gif)"
        expected = [("alt text", "https://i.imgur.com/aKaOqIh%20with%20spaces.gif")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
        
class TestExtractMarkdownLinks(unittest.TestCase):
    
    def test_single_link(self):
        text = "This is text with a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
    
    def test_multiple_links(self):
        text = "This is text with a [link](https://example.com) and [another link](https://example.com/another)"
        expected = [("link", "https://example.com"), ("another link", "https://example.com/another")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

        
class TestSplitNodesImage(unittest.TestCase):
    
    def test_single_image_org(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        expected = [node]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_image_with_no_alt_text(self):
        node = TextNode("This is text with an image ![](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_image_with_special_characters_in_alt_text(self):
        node = TextNode("This is text with an image ![alt text with special characters !@#$%^&*()](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text with special characters !@#$%^&*()", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_image_with_spaces_in_url(self):
        node = TextNode("This is text with an image ![alt text](https://i.imgur.com/aKaOqIh%20with%20spaces.gif)", TextType.TEXT)
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/aKaOqIh%20with%20spaces.gif")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)
        
class TestSplitNodesLink(unittest.TestCase):
    
    def test_single_link_org(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_single_link(self):
        node = TextNode("This is text with a [link](https://example.com)", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode("This is text with a [link](https://example.com) and [another link](https://example.com/another)", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://example.com/another")
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        expected = [node]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_link_with_special_characters(self):
        node = TextNode("This is text with a [link with special characters !@#$%^&*()](https://example.com)", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link with special characters !@#$%^&*()", TextType.LINK, "https://example.com")
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_link_with_spaces_in_url(self):
        node = TextNode("This is text with a [link](https://example.com/with%20spaces)", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/with%20spaces")
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_no_special_formatting(self):
        text = "This is plain text with no special formatting."
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("This is plain text with no special formatting.", TextType.TEXT)]
        self.assertEqual(text_nodes, expected)

    def test_text_with_only_bold(self):
        text = "This is **bold** text."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_only_italic(self):
        text = "This is *italic* text."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_only_code(self):
        text = "This is `code` text."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_only_image(self):
        text = "This is an ![image](https://example.com/image.jpg) in text."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" in text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_only_link(self):
        text = "This is a [link](https://example.com) in text."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_multiple_bold_and_italic(self):
        text = "This is **bold** and *italic* text."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_nested_formatting(self):
        text = "This is **bold and *italic* text**."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold and ", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_multiple_images_and_links(self):
        text = "This is text with an ![image1](https://example.com/image1.jpg) and a [link1](https://example.com/link1) and another ![image2](https://example.com/image2.jpg) and another [link2](https://example.com/link2)."
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/image1.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/link1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/image2.jpg"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/link2"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected)

    def test_text_with_empty_string(self):
        text = ""
        text_nodes = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(text_nodes, expected)

        
if __name__ == '__main__':
    unittest.main()
