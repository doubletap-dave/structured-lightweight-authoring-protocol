import re
from pathlib import Path

from src.nomenic.lexer import Lexer
from src.nomenic.tokens import TokenType

content = Path("tests/fixtures/sample.nmc").read_text()
lexer = Lexer(content)
tokens = list(lexer.tokenize())

# Find all style tokens
print("Looking for style tokens:")
style_tokens = [
    t
    for t in tokens
    if t.type
    in (
        TokenType.STYLE_BOLD,
        TokenType.STYLE_ITALIC,
        TokenType.STYLE_CODE,
        TokenType.STYLE_LINK,
    )
]
print(f"Found {len(style_tokens)} style tokens")
for t in style_tokens:
    print(f"  {t}")

# Look at regex patterns
print("\nTesting regex patterns directly:")
test_text = (
    "This text has @b(bold), @i(italic), and @c(code) styles. "
    "Here's a @l(link) to something."
)
print(f"Test text: {test_text}")

re_style_bold = re.compile(r"@b\(([^)]*)\)|@bold\(([^)]*)\)")
re_style_italic = re.compile(r"@i\(([^)]*)\)|@italic\(([^)]*)\)")
re_style_code = re.compile(r"@c\(([^)]*)\)|@code\(([^)]*)\)")
re_style_link = re.compile(r"@l\(([^)]*)\)|@link\(([^)]*)\)")

bold_matches = list(re_style_bold.finditer(test_text))
italic_matches = list(re_style_italic.finditer(test_text))
code_matches = list(re_style_code.finditer(test_text))
link_matches = list(re_style_link.finditer(test_text))

print(f"Found {len(bold_matches)} bold matches")
for m in bold_matches:
    print(f"  Match: {m.group(0)}, Content: {m.group(1) or m.group(2)}")

print(f"Found {len(italic_matches)} italic matches")
for m in italic_matches:
    print(f"  Match: {m.group(0)}, Content: {m.group(1) or m.group(2)}")

print(f"Found {len(code_matches)} code matches")
for m in code_matches:
    print(f"  Match: {m.group(0)}, Content: {m.group(1) or m.group(2)}")

print(f"Found {len(link_matches)} link matches")
for m in link_matches:
    print(f"  Match: {m.group(0)}, Content: {m.group(1) or m.group(2)}")

# Find where the inline styles are in the sample file
lines = content.splitlines()
for i, line in enumerate(lines):
    if "@" in line:
        print(f"\nLine {i+1} with @: {line}")
        text_tokens = [
            t for t in tokens if t.type == TokenType.TEXT and t.line == i + 1
        ]
        for t in text_tokens:
            print(f"  Text token at this line: {t}")
