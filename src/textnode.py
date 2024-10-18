from enum import Enum
from typing import Optional

class TextType(Enum):
    """
    TextType is an enumeration that defines different types of nodes that can be used in a static site generator.

    Attributes:
        TEXT (str): Represents a text node.
        BOLD (str): Represents a bold text node.
        ITALIC (str): Represents an italic text node.
        CODE (str): Represents a code block node.
        LINK (str): Represents a hyperlink node.
        IMAGE (str): Represents an image node.
    """
    TEXT = "text" # Represents a text node in the document.
    BOLD = "bold" # Represents a bold text node in the document with **text**.
    ITALIC = "italic" # Represents an italic text node in the document with *text*.
    CODE = "code" # Represents a code block node in the document with `code`.
    LINK = "link" # Represents a hyperlink node in the document with [text](url).
    IMAGE = "image" # Represents an image node in the document with ![text](url).

class TextNode:
    """
    A class to represent a text node with optional URL.

    Attributes:
    -----------
    text : str
        The text content of the node.
    text_type : str
        The type of the text, derived from the provided enum value.
    url : Optional[str]
        An optional URL associated with the text node.

    Methods:
    --------
    __init__(text: str, text_type_enum: TextType, url: Optional[str] = None):
        Initializes the TextNode with text, text type, and optional URL.
    __eq__(other: 'TextNode') -> bool:
        Checks equality between two TextNode instances based on text, text type, and URL.
    __repr__() -> str:
        Returns a string representation of the TextNode instance.
    """
    def __init__(self, text: str, text_type_enum: TextType, url: Optional[str] = None):
        if not isinstance(text_type_enum, TextType):
            raise ValueError("text_type_enum must be an instance of TextType")
        self.text = text
        self.text_type = text_type_enum.value
        self.url = url
    
    def __eq__(self, other: 'TextNode') -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
