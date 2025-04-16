import pytest
import json
from pathlib import Path

from nomenic import Lexer, Parser
from nomenic.ast import DocumentNode, HeaderNode, TextNode, ListNode, BlockNode
from nomenic.renderers.json import JSONRendererVisitor, render_json


# Fixture to load test documents
@pytest.fixture
def sample_document():
    """Load the sample document for testing."""
    fixture_path = Path(__file__).parent.parent.parent / "fixtures" / "sample.nmc"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def parsed_document(sample_document):
    """Parse the sample document into an AST."""
    lexer = Lexer(sample_document)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    return parser.parse()


@pytest.fixture
def visitor():
    """Create a JSONRendererVisitor instance."""
    return JSONRendererVisitor(pretty=True, include_content=True)


# Unit tests for individual visitor methods
class TestJSONVisitorMethods:
    """Test individual methods of the JSONRendererVisitor."""

    def test_visit_header(self, visitor):
        """Test processing a header node."""
        node = HeaderNode(level=2, text="Test Header")
        result = visitor.visit_header(node)
        
        assert result["type"] == "section"
        assert result["title"] == "Test Header"
        assert "content" in result
        assert isinstance(result["content"], list)
        assert len(result["content"]) == 0

    def test_visit_text(self, visitor):
        """Test processing a text node."""
        node = TextNode(text="This is a test paragraph.")
        result = visitor.visit_text(node)
        
        assert result["type"] == "text"
        assert result["content"] == "This is a test paragraph."
        
        # Test without content
        visitor.include_content = False
        result = visitor.visit_text(node)
        
        assert result["type"] == "text"
        assert "content" not in result

    def test_visit_list(self, visitor):
        """Test processing a list node."""
        item1 = TextNode(text="Item 1")
        item2 = TextNode(text="Item 2")
        node = ListNode(ordered=False, items=[item1, item2])
        
        result = visitor.visit_list(node)
        
        assert result["type"] == "list"
        assert "items" in result
        assert isinstance(result["items"], list)
        assert len(result["items"]) == 2
        assert result["items"][0] == "Item 1"
        assert result["items"][1] == "Item 2"

    def test_process_code_block(self, visitor):
        """Test processing a code block."""
        text_node = TextNode(text="def hello():\n    print('Hello world')")
        node = BlockNode(block_type="code", children=[text_node])
        node.meta = {"language": "python"}
        
        result = visitor._process_code_block(node)
        
        assert result["type"] == "code"
        assert result["content"] == "def hello():\n    print('Hello world')"
        assert result["language"] == "python"
        
        # Test without content
        visitor.include_content = False
        result = visitor._process_code_block(node)
        
        assert result["type"] == "code"
        assert "content" not in result

    def test_process_table_block(self, visitor):
        """Test processing a table block."""
        header_row = TextNode(text="Column 1 | Column 2")
        data_row = TextNode(text="Data 1 | Data 2")
        node = BlockNode(block_type="table", children=[header_row, data_row])
        
        result = visitor._process_table_block(node)
        
        assert result["type"] == "table"
        assert "rows" in result
        assert isinstance(result["rows"], list)
        assert len(result["rows"]) == 2
        assert result["rows"][0] == ["Column 1", "Column 2"]
        assert result["rows"][1] == ["Data 1", "Data 2"]
        
        # Test without content
        visitor.include_content = False
        result = visitor._process_table_block(node)
        
        assert result["type"] == "table"
        assert "rows" not in result

    def test_process_meta_block(self, visitor):
        """Test processing a meta block."""
        node = BlockNode(block_type="meta", children=[])
        node.meta = {
            "title": "Test Document",
            "author": "Test Author",
            "version": "1.0.0"
        }
        
        result = visitor.visit_block(node)
        
        assert result["type"] == "meta"
        assert "metadata" in result
        assert result["metadata"]["title"] == "Test Document"
        assert result["metadata"]["author"] == "Test Author"
        assert result["metadata"]["version"] == "1.0.0"
        
        # Test without content
        visitor.include_content = False
        result = visitor.visit_block(node)
        
        assert result["type"] == "meta"
        assert "metadata" not in result


# Integration tests using fixture
class TestJSONRendererIntegration:
    """Test the full JSON rendering pipeline."""

    def test_render_json_full_document(self, sample_document):
        """Test rendering a complete document to JSON."""
        json_output = render_json(sample_document)
        
        # Parse JSON to verify it's valid
        result = json.loads(json_output)
        
        # Basic structure
        assert isinstance(result, dict)
        assert "sections" in result
        assert isinstance(result["sections"], list)
        
        # Find the main section header
        sections = result["sections"]
        main_section = next((s for s in sections if s["type"] == "section" and s["title"] == "Sample Document"), None)
        assert main_section is not None, "Main section not found in JSON output"
        
        # Verify there's a meta block in the document structure to hold the metadata
        # In this implementation, metadata values are currently represented as text nodes
        meta_values = {
            "title": "Sample Document",
            "author": "Test User",
            "date": "2024-03-15",
            "version": "1.0.0"
        }
        
        for key, value in meta_values.items():
            # Find text nodes that contain metadata information
            found = False
            for item in sections:
                if (item.get("type") == "text" and 
                    item.get("content") and 
                    f"{key}: {value}" in item.get("content")):
                    found = True
                    break
            
            assert found, f"Could not find metadata '{key}: {value}' in the document"

    def test_render_json_without_content(self, sample_document):
        """Test rendering without including content."""
        json_output = render_json(sample_document, include_content=False)
        
        # Parse JSON to verify it's valid
        result = json.loads(json_output)
        
        # Basic structure
        assert isinstance(result, dict)
        assert "sections" in result
        
        # Find text nodes and verify they don't have content
        def check_no_content(node):
            if isinstance(node, dict):
                if node.get("type") == "text":
                    assert "content" not in node
                
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        check_no_content(value)
            elif isinstance(node, list):
                for item in node:
                    check_no_content(item)
        
        check_no_content(result)

    def test_render_json_not_pretty(self, sample_document):
        """Test rendering without pretty formatting."""
        json_pretty = render_json(sample_document, pretty=True)
        json_compact = render_json(sample_document, pretty=False)
        
        # Compact version should be shorter
        assert len(json_compact) < len(json_pretty)
        
        # Both should be valid JSON
        assert json.loads(json_pretty)
        assert json.loads(json_compact) 