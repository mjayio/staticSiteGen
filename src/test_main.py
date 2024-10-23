import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title_with_title(self):
        markdown = "# My Title\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_with_multiple_titles(self):
        markdown = "# My Title\nSome content here.\n# Another Title"
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_with_no_title(self):
        markdown = "Some content here without a title."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_extract_title_with_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown")

    def test_extract_title_with_only_title(self):
        markdown = "# My Title"
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")
        

if __name__ == '__main__':
    unittest.main()