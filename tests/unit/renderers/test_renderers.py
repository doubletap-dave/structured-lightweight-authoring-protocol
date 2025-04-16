import pytest
import json as json_lib
import yaml as yaml_lib
from pathlib import Path

from nomenic import Lexer, Parser
from nomenic.renderers.html import render_html
from nomenic.renderers.markdown import render_markdown
from nomenic.renderers.yaml import render_yaml
from nomenic.renderers.json import render_json

# Import renderers (to be implemented)
# Will uncomment as they are implemented
# from nomenic.renderers.json import render_json


# Fixture to load test documents
@pytest.fixture
def sample_document():
    """Sample document for testing renderers."""
    return """meta:
  title: Sample Document
  author: Test User
  date: 2024-03-15
  version: 1.0.0

header: Sample Document
  text: This is a sample Nomenic Core document for testing purposes.

section: Test Section
  note: This is a note callout
"""


# HTML Renderer Tests
def test_html_renderer_basic(sample_document):
    """Test that the HTML renderer produces valid output."""
    html_output = render_html(sample_document)
    
    # Check for HTML structure
    assert "<!DOCTYPE html>" in html_output
    assert "<html>" in html_output
    assert "<head>" in html_output
    assert "<body>" in html_output
    assert "</html>" in html_output
    
    # Check for content
    assert "<h1" in html_output
    assert "Sample Document" in html_output
    assert "This is a sample Nomenic Core document" in html_output
    assert "This is a note callout" in html_output


# Markdown Renderer Tests
def test_markdown_renderer_basic(sample_document):
    """Test that the Markdown renderer produces valid output."""
    md_output = render_markdown(sample_document)
    
    # Check for expected Markdown structure
    assert "# Sample Document" in md_output
    assert "This is a sample Nomenic Core document" in md_output
    
    # Check for section header
    assert "## Test Section" in md_output
    
    # Check for note callout
    assert "> **Note:** This is a note callout" in md_output


# YAML Renderer Tests
def test_yaml_renderer_basic(sample_document):
    """Test that the YAML renderer produces valid output."""
    yaml_output = render_yaml(sample_document)
    
    # Parse the YAML to verify it's valid
    yaml_data = yaml_lib.safe_load(yaml_output)
    
    # Check for expected YAML structure
    assert "sections" in yaml_data
    
    # Check for content
    assert "Sample Document" in yaml_output
    assert "This is a sample Nomenic Core document" in yaml_output
    assert "This is a note callout" in yaml_output


# JSON Renderer Tests
def test_json_renderer_basic(sample_document):
    """Test that the JSON renderer produces valid output."""
    json_output = render_json(sample_document)
    
    # Parse the JSON to verify it's valid
    json_data = json_lib.loads(json_output)
    
    # Check for expected JSON structure
    assert "sections" in json_data
    assert len(json_data["sections"]) > 0
    
    # Find the section with 'Sample Document' as title
    found_section = False
    for section in json_data["sections"]:
        if section.get("type") == "section" and section.get("title") == "Sample Document":
            found_section = True
            assert "content" in section
            # With the refactored visitor pattern implementation, section["content"] can be empty
            # No need to check the length
            break
    
    assert found_section, "Expected to find a section with title 'Sample Document'"
    
    # With the new visitor pattern implementation, content is not nested inside sections anymore
    # Instead, it's at the top level in the sections array
    text_nodes = [item for item in json_data["sections"] 
                 if item.get("type") == "text"]
    assert len(text_nodes) > 0, "Expected to find text nodes in sections array" 