from nomenic.ast import BlockNode, DocumentNode, HeaderNode, ListNode, TextNode
from nomenic.lexer import tokenize
from nomenic.parser import parse

# Constants for test assertions
HEADER_AND_TEXT_COUNT = 2
LIST_ITEM_COUNT = 3
TABLE_ROW_COUNT = 2
CALLOUT_COUNT = 2
BLOCKQUOTE_LINE_COUNT = 2
FIGURE_PARTS_COUNT = 2
CUSTOM_DIRECTIVE_PARTS_COUNT = 1
DEF_LIST_PARTS_COUNT = 4


def test_parse_header_and_text():
    source = """
header: Welcome to Nomenic
text: This is a test paragraph.
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == HEADER_AND_TEXT_COUNT
    header = ast.children[0]
    text = ast.children[1]
    assert isinstance(header, HeaderNode)
    assert header.text == "Welcome to Nomenic"
    assert isinstance(text, TextNode)
    assert text.text == "This is a test paragraph."


def test_parse_unordered_list():
    source = """
list:
- First item
- Second item
- Third item
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one ListNode child
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    list_node = ast.children[0]
    assert isinstance(list_node, ListNode)
    assert not list_node.ordered
    assert len(list_node.items) == LIST_ITEM_COUNT
    assert all(isinstance(item, TextNode) for item in list_node.items)
    assert [item.text for item in list_node.items] == [
        "First item",
        "Second item",
        "Third item",
    ]


def test_parse_ordered_list():
    source = """
list:
1. First item
a. Second item
i. Third item
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one ListNode child
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    list_node = ast.children[0]
    assert isinstance(list_node, ListNode)
    assert list_node.ordered
    assert len(list_node.items) == LIST_ITEM_COUNT
    assert all(isinstance(item, TextNode) for item in list_node.items)
    assert [item.text for item in list_node.items] == [
        "First item",
        "Second item",
        "Third item",
    ]


def test_parse_code_block():
    source = """
code:
    def hello():
        return 'world'
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one BlockNode child (block_type='code')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    code_node = ast.children[0]
    assert isinstance(code_node, BlockNode)
    assert code_node.block_type == "code"
    assert len(code_node.children) == 1
    code_text = code_node.children[0]
    assert isinstance(code_text, TextNode)
    assert "def hello()" in code_text.text
    assert "return 'world'" in code_text.text


def test_parse_table_block():
    source = """
table:
- row: Header1, Header2
- row: Value1, Value2
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one BlockNode child (block_type='table')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    table_node = ast.children[0]
    from nomenic.ast import BlockNode, TextNode

    assert isinstance(table_node, BlockNode)
    assert table_node.block_type == "table"
    assert len(table_node.children) == TABLE_ROW_COUNT
    assert all(isinstance(row, TextNode) for row in table_node.children)
    assert table_node.children[0].text == "Header1, Header2"
    assert table_node.children[1].text == "Value1, Value2"


def test_parse_callout_block():
    source = """
note: This is an important note.
warn: This is a warning.
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with two BlockNode children (block_type='callout')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == CALLOUT_COUNT
    from nomenic.ast import BlockNode, TextNode

    note_node = ast.children[0]
    warn_node = ast.children[1]
    assert isinstance(note_node, BlockNode)
    assert note_node.block_type == "callout"
    assert len(note_node.children) == 1
    assert isinstance(note_node.children[0], TextNode)
    assert "important note" in note_node.children[0].text
    assert isinstance(warn_node, BlockNode)
    assert warn_node.block_type == "callout"
    assert len(warn_node.children) == 1
    assert isinstance(warn_node.children[0], TextNode)
    assert "warning" in warn_node.children[0].text


def test_parse_blockquote_block():
    source = """
blockquote:
> This is a quoted line.
> Another quoted line.
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one BlockNode child (block_type='blockquote')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    from nomenic.ast import BlockNode, TextNode

    blockquote_node = ast.children[0]
    assert isinstance(blockquote_node, BlockNode)
    assert blockquote_node.block_type == "blockquote"
    assert len(blockquote_node.children) == BLOCKQUOTE_LINE_COUNT
    assert all(isinstance(line, TextNode) for line in blockquote_node.children)
    assert blockquote_node.children[0].text == "This is a quoted line."
    assert blockquote_node.children[1].text == "Another quoted line."


def test_parse_figure_block():
    source = """
figure:
src: /images/example.png
caption: Example Figure
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one BlockNode child (block_type='figure')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    from nomenic.ast import BlockNode, TextNode

    figure_node = ast.children[0]
    assert isinstance(figure_node, BlockNode)
    assert figure_node.block_type == "figure"
    assert len(figure_node.children) == FIGURE_PARTS_COUNT
    assert isinstance(figure_node.children[0], TextNode)
    assert figure_node.children[0].text == "/images/example.png"
    assert isinstance(figure_node.children[1], TextNode)
    assert figure_node.children[1].text == "Example Figure"


def test_parse_custom_directive_block():
    source = """
x-foo:
Custom directive content.
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one BlockNode child (block_type='x-foo')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    from nomenic.ast import BlockNode, TextNode

    custom_node = ast.children[0]
    assert isinstance(custom_node, BlockNode)
    assert custom_node.block_type == "x-foo"
    assert len(custom_node.children) == CUSTOM_DIRECTIVE_PARTS_COUNT
    assert isinstance(custom_node.children[0], TextNode)
    assert "Custom directive content." in custom_node.children[0].text


def test_parse_definition_list_block():
    source = """
def-list:
dt: Term 1
dd: Description 1
dt: Term 2
dd: Description 2
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one BlockNode child (block_type='def-list')
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    from nomenic.ast import BlockNode, TextNode

    deflist_node = ast.children[0]
    assert isinstance(deflist_node, BlockNode)
    assert deflist_node.block_type == "def-list"
    assert len(deflist_node.children) == DEF_LIST_PARTS_COUNT
    assert isinstance(deflist_node.children[0], TextNode)
    assert deflist_node.children[0].text == "Term 1"
    assert isinstance(deflist_node.children[1], TextNode)
    assert deflist_node.children[1].text == "Description 1"
    assert isinstance(deflist_node.children[2], TextNode)
    assert deflist_node.children[2].text == "Term 2"
    assert isinstance(deflist_node.children[3], TextNode)
    assert deflist_node.children[3].text == "Description 2"


def test_parse_multiline_text_block():
    source = """
text:
>>>
This is a paragraph.
It spans multiple lines.
<<<
"""
    tokens = tokenize(source)
    ast = parse(tokens)
    # Should produce a DocumentNode with one TextNode child containing
    # the full multi-line text
    assert isinstance(ast, DocumentNode)
    assert len(ast.children) == 1
    from nomenic.ast import TextNode

    text_node = ast.children[0]
    assert isinstance(text_node, TextNode)
    assert "This is a paragraph." in text_node.text
    assert "It spans multiple lines." in text_node.text
    assert "\n" in text_node.text  # Should preserve newlines
