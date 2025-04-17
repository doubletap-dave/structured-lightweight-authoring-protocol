from nomenic import Lexer, Parser

def format_node_value(node):
    """Extract and format the primary value from a node."""
    if hasattr(node, "text") and node.text:
        return f"text: {node.text}"
    elif hasattr(node, "block_type") and node.block_type:
        return f"block_type: {node.block_type}"
    elif hasattr(node, "name") and node.name:
        return f"name: {node.name}"
    else:
        attrs = [attr for attr in dir(node) if not attr.startswith('_') and not callable(getattr(node, attr))]
        values = {attr: getattr(node, attr) for attr in attrs if getattr(node, attr)}
        if values:
            return f"attributes: {values}"
        return "no primary value"

def print_ast_node(node, indent=0, index=None, parent_type=None):
    """Recursively print an AST node and its children with detailed information."""
    prefix = " " * indent
    node_type = type(node).__name__
    
    # Format node information
    node_info = format_node_value(node)
    index_str = f"{index}: " if index is not None else ""
    parent_info = f" (parent: {parent_type})" if parent_type else ""
    
    print(f"{prefix}{index_str}{node_type}{parent_info} - {node_info}")
    
    # Print additional attributes for debugging
    if hasattr(node, "attributes") and node.attributes:
        print(f"{prefix}  Attributes: {node.attributes}")
    
    # Recursively print children
    if hasattr(node, "children") and node.children:
        print(f"{prefix}  Children ({len(node.children)}):")
        for i, child in enumerate(node.children):
            print_ast_node(child, indent + 4, i, node_type)

def main():
    # Read the sample file
    filepath = 'tests/fixtures/sample.nmc'
    content = open(filepath).read()
    
    # Parse the content
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    doc = parser.parse()
    
    # Print header information
    print(f"AST Analysis for: {filepath}")
    print("=" * 50)
    print(f"Document Type: {type(doc).__name__}")
    print(f"Total Nodes: {len(doc.children)}")
    print("=" * 50)
    
    # Print token information
    print("\nTokens Summary:")
    token_types = {}
    for token in tokens:
        token_type = token.type
        token_types[token_type] = token_types.get(token_type, 0) + 1
    
    for token_type, count in token_types.items():
        print(f"  {token_type}: {count}")
    
    # Print AST structure
    print("\nAST Structure:")
    print("=" * 50)
    for i, node in enumerate(doc.children):
        print_ast_node(node, indent=0, index=i)

if __name__ == "__main__":
    main() 