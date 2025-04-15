from nomenic.ast import BlockNode, HeaderNode, TextNode
from nomenic.lexer import tokenize
from nomenic.parser import Parser, parse

# Constants for test assertions
META_BLOCK_INDEX = 0
HEADER_INDEX = 1
TEXT_INDEX = 2
LIST_INDEX = 3
EXPECTED_NODE_COUNT_WITH_META = 3
EXPECTED_NODE_COUNT_WITH_MERGED_TEXT = 2
EXPECTED_NODE_COUNT_WITH_LIST = 4
EXPECTED_LIST_ITEMS = 2


def test_validation_catches_missing_meta():
    """Test that validation flags documents missing a meta block."""
    source = """
header: Welcome to Nomenic
text: This is a test paragraph.
"""
    tokens = tokenize(source)
    parser = Parser(tokens)
    document = parser.parse()

    # Check validation
    validation_errors = parser.validate_document(document)
    assert len(validation_errors) > 0
    # First error should be about missing meta block
    assert "meta block" in validation_errors[0][0].lower()


def test_validation_checks_meta_version():
    """Test that validation ensures meta block has version info."""
    source = """
meta: author=Test
header: Welcome to Nomenic
"""
    tokens = tokenize(source)
    parser = Parser(tokens)
    document = parser.parse()

    # Check validation
    validation_errors = parser.validate_document(document)
    assert len(validation_errors) > 0
    # First error should be about missing version
    assert "version" in validation_errors[0][0].lower()


def test_document_with_valid_meta():
    """Test that a document with valid meta passes validation."""
    source = """
meta: version=1.0.0, author=Test
header: Welcome to Nomenic
"""
    tokens = tokenize(source)
    parser = Parser(tokens)
    document = parser.parse()

    # Check validation
    validation_errors = parser.validate_document(document)
    assert len(validation_errors) == 0


def test_normalization_removes_empty_text():
    """Test that normalization removes empty text nodes."""
    source = """
meta: version=1.0.0
header: Test
text:
text: Non-empty content
"""
    tokens = tokenize(source)
    parser = Parser(tokens)
    document = parser.parse()

    # The empty text node is already filtered out by the parser
    # So we should have 3 nodes: meta, header, non-empty text
    assert len(document.children) == EXPECTED_NODE_COUNT_WITH_META

    # Apply normalization
    normalized = document.normalize()

    # After normalization, structure should remain the same
    # meta, header, non-empty text
    assert len(normalized.children) == EXPECTED_NODE_COUNT_WITH_META

    # Verify the non-empty text remains
    text_nodes = [node for node in normalized.children if isinstance(node, TextNode)]
    assert len(text_nodes) == 1
    assert "Non-empty content" in text_nodes[0].text


def test_optimization_merges_adjacent_text():
    """Test that optimization merges adjacent text nodes."""
    source = """
meta: version=1.0.0
text: First paragraph.
text: Second paragraph.
"""
    tokens = tokenize(source)
    document = parse(tokens)  # This already applies normalize() and optimize()

    # After optimization
    # meta and merged text
    assert len(document.children) == EXPECTED_NODE_COUNT_WITH_MERGED_TEXT

    # Verify text nodes were merged
    text_nodes = [node for node in document.children if isinstance(node, TextNode)]
    assert len(text_nodes) == 1
    assert "First paragraph." in text_nodes[0].text
    assert "Second paragraph." in text_nodes[0].text


def test_optimization_preserves_structure():
    """Test that optimization preserves overall document structure."""
    source = """
meta: version=1.0.0
header: Section 1
text: Some content.
list:
- Item 1
- Item 2
"""
    tokens = tokenize(source)
    document = parse(tokens)  # This already applies normalize() and optimize()

    # Check structure is preserved
    # meta, header, text, list
    assert len(document.children) == EXPECTED_NODE_COUNT_WITH_LIST

    # Check node types
    assert isinstance(document.children[META_BLOCK_INDEX], BlockNode)  # meta
    assert document.children[META_BLOCK_INDEX].block_type == "meta"
    assert isinstance(document.children[HEADER_INDEX], HeaderNode)
    assert isinstance(document.children[TEXT_INDEX], TextNode)

    # List node should be preserved as ListNode (not BlockNode)
    from nomenic.ast import ListNode

    list_node = document.children[LIST_INDEX]
    assert isinstance(list_node, ListNode)
    assert len(list_node.items) == EXPECTED_LIST_ITEMS
