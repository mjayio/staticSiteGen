class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        tag_values = []
        for tag, value in self.props.items():
            tag_values.append(f"{tag}={value}")
        return " ".join(tag_values)



    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value \
                and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
