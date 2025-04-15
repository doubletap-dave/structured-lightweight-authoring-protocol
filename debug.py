import re
from pathlib import Path

from src.nomenic.tokens import TOKEN_MAP

content = Path("tests/fixtures/sample.nmc").read_text()
first_line = content.splitlines()[0]
print(f"First line: '{first_line}'")

# Test with original regex (requiring whitespace)
re_block_token_strict = re.compile(r"^([a-zA-Z0-9_-]+):\s+")
strict_match = re_block_token_strict.match(first_line)
print(f"Matches strict regex (with whitespace): {bool(strict_match)}")

# Test with modified regex (optional whitespace)
re_block_token_flexible = re.compile(r"^([a-zA-Z0-9_-]+):\s*")
flexible_match = re_block_token_flexible.match(first_line)
print(f"Matches flexible regex (optional whitespace): {bool(flexible_match)}")

if flexible_match:
    token_key = flexible_match.group(1)
    token_str = f"{token_key}:"
    print(f"Token key: '{token_key}'")
    print(f"Token str: '{token_str}'")
    print(f"TOKEN_MAP keys: {list(TOKEN_MAP.keys())}")
    print(f"'{token_str}' in TOKEN_MAP: {token_str in TOKEN_MAP}")
