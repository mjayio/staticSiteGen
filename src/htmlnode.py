import functools


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        tag_values = []
        for tag, value in self.props.items():
            tag_values.append(f"{tag}=\"{value}\"")
        return " " + " ".join(tag_values)

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value \
                and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag == None or self.tag == "":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or not self.tag:
            raise ValueError("All parent nodes must have a tag.")
        if not self.children or not isinstance(self.children, list):
            raise ValueError("All parent nodes must have a children list.")
        return f"<{self.tag}{self.props_to_html()}>" + functools.reduce(lambda x, y: x + y.to_html(), self.children, "") + f"</{self.tag}>"
