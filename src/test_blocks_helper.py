import unittest
from blocks_helper import BlockType, block_to_block_type, block_to_html, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_mixed_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = ["# This is a heading", 
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
                    """* This is the first list item in a list block
* This is a list item
* This is another list item"""]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block(self):
        markdown = "This is a single block of text."
        expected = ["This is a single block of text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blocks(self):
        markdown = "This is the first block.\n\nThis is the second block."
        expected = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blocks_with_extra_whitespace(self):
        markdown = "  This is the first block.  \n\n  This is the second block.  "
        expected = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = [""]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_only_whitespace(self):
        markdown = "   "
        expected = [""]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blank_lines(self):
        markdown = "This is the first block.\n\n\n\nThis is the second block."
        expected = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_no_blank_lines(self):
        markdown = "This is the first block.\nThis is still the first block."
        expected = ["This is the first block.\nThis is still the first block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)
        

class TestBlockToBlockType(unittest.TestCase):

    def test_heading1_block(self):
        markdown_block = "# Heading 1"
        expected = BlockType.HEADING1
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_heading2_block(self):
        markdown_block = "## Heading 2"
        expected = BlockType.HEADING2
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_heading3_block(self):
        markdown_block = "### Heading 3"
        expected = BlockType.HEADING3
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_heading4_block(self):
        markdown_block = "#### Heading 4"
        expected = BlockType.HEADING4
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_heading5_block(self):
        markdown_block = "##### Heading 5"
        expected = BlockType.HEADING5
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_heading6_block(self):
        markdown_block = "###### Heading 6"
        expected = BlockType.HEADING6
        self.assertEqual(block_to_block_type(markdown_block), expected)
    
    def test_heading_block(self):
        markdown_block = "# This is a heading"
        expected = BlockType.HEADING1
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_code_block(self):
        markdown_block = "```\nThis is a code block\n```"
        expected = BlockType.CODE
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_quote_block(self):
        markdown_block = "> This is a quote"
        expected = BlockType.QUOTE
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_unordered_list_block(self):
        markdown_block = "* This is an unordered list item"
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_ordered_list_block(self):
        markdown_block = "1. This is an ordered list item"
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_paragraph_block(self):
        markdown_block = "This is a paragraph."
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_heading_with_multiple_hashes(self):
        markdown_block = "### This is a level 3 heading"
        expected = BlockType.HEADING3
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_code_block_with_extra_backticks(self):
        markdown_block = "````\nThis is a code block with extra backticks\n````"
        expected = BlockType.CODE
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_unordered_list_with_hyphen(self):
        markdown_block = "- This is an unordered list item with a hyphen"
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(markdown_block), expected)

    def test_ordered_list_with_multiple_digits(self):
        markdown_block = "123. This is an ordered list item with multiple digits"
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(markdown_block), expected)
        
    def test_ill_formatted_ordered_list_is_paragraph(self):
            markdown_block = "123.This is an ordered list item with multiple digits"
            expected = BlockType.PARAGRAPH
            self.assertEqual(block_to_block_type(markdown_block), expected)
            
            
class TestBlockToHTML(unittest.TestCase):

    def test_heading1_to_html(self):
        markdown = "# Heading 1"
        expected = ParentNode("div", [ParentNode("h1", [HTMLNode("", "Heading 1")])])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

    def test_paragraph_to_html(self):
        markdown = "This is a paragraph."
        expected = ParentNode("div", [ParentNode("p", [HTMLNode("", "This is a paragraph.")])])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

    def test_code_block_to_html(self):
        markdown = "```\nThis is a code block\n```"
        expected = ParentNode("div", [ParentNode("code", [HTMLNode("", "This is a code block")])])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

    def test_quote_block_to_html(self):
        markdown = "> This is a quote"
        expected = ParentNode("div", [ParentNode("blockquote", [HTMLNode("", "This is a quote")])])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

    def test_unordered_list_to_html(self):
        markdown = "* This is an unordered list item"
        expected = ParentNode("div", [ParentNode("ul", [HTMLNode("li", "This is an unordered list item")])])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

    def test_ordered_list_to_html(self):
        markdown = "1. This is an ordered list item"
        expected = ParentNode("div", [ParentNode("ol", [HTMLNode("li", "This is an ordered list item")])])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

    def test_mixed_blocks_to_html(self):
        markdown = """# Heading 1

This is a paragraph.

* List item 1
* List item 2

1. Ordered item 1
2. Ordered item 2"""
        expected = ParentNode("div", [
            ParentNode("h1", [HTMLNode("", "Heading 1")]),
            ParentNode("p", [HTMLNode("", "This is a paragraph.")]),
            ParentNode("ul", [HTMLNode("li", "List item 1"), HTMLNode("li", "List item 2")]),
            ParentNode("ol", [HTMLNode("li", "Ordered item 1"), HTMLNode("li", "Ordered item 2")]),
        ])
        result = block_to_html(markdown)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()