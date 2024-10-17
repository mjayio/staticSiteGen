import functools
from typing import List, Dict, Optional, Union

class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List['HTMLNode']] = None, props: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self) -> str:
        raise NotImplementedError("Subclasses must implement to_html method.")
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        tag_values = [f'{tag}="{value}"' for tag, value in self.props.items()]
        return " " + " ".join(tag_values)

    def __eq__(self, other: 'HTMLNode') -> bool:
        return self.tag == other.tag and self.value == other.value \
                and self.children == other.children and self.props == other.props
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Optional[Dict[str, str]] = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, str]] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")
        if not isinstance(self.children, list):
            raise ValueError("All parent nodes must have a children list.")
        children_html = functools.reduce(lambda x, y: x + y.to_html(), self.children, "")
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
