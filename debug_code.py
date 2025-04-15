from pathlib import Path

from src.nomenic.lexer import Lexer
from src.nomenic.tokens import TokenType

content = Path("tests/fixtures/sample.nmc").read_text()
lexer = Lexer(content)
tokens = list(lexer.tokenize())

# Print all tokens related to code blocks
print("Searching for CODE tokens...")
code_tokens = [t for t in tokens if t.type == TokenType.CODE]
print(f"Found {len(code_tokens)} CODE tokens")

# Look for 'code:' in any token value
print("\nSearching for 'code:' in token values...")
code_str_tokens = [t for t in tokens if t.value == "code:"]
print(f"Found {len(code_str_tokens)} tokens with value 'code:'")
for t in code_str_tokens:
    print(f"  Token: {t}")

# Find relevant lines in the sample file
lines = content.splitlines()
for i, line in enumerate(lines):
    if "code:" in line:
        print(f"\nFound 'code:' at line {i+1}: {line}")
        # Print context (2 lines before and after)
        start = max(0, i - 2)
        end = min(len(lines), i + 3)
        print("\nContext:")
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}")
