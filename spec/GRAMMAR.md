# Nomenic Core v1.0.0 EBNF Grammar

This document provides a formal Extended Backus-Naur Form (EBNF) definition for the Nomenic Core v1.0.0 syntax.

## Notation

*   `=` : Definition
*   `|` : Alternation (OR)
*   `{ ... }` : Repetition (0 or more times)
*   `[ ... ]` : Optional (0 or 1 time)
*   `( ... )` : Grouping
*   `'...'` : Terminal literal string
*   `UPPERCASE` : Terminal token type (defined in `TOKEN-SCHEMA.nmc`)
*   `lowercase` : Non-terminal rule name

## Grammar Rules

(* Note: This grammar assumes a pre-processing step or lexer handles indentation levels and identifies basic token types like IDENTIFIER, STRING, etc., based on `TOKEN-SCHEMA.nmc`. *)

document       = { meta_block } , { block } ;

block          = indented_block | top_level_block ;

indented_block = INDENT, ( header_block | text_block | list_block | code_block | table_block | directive_block | extended_block | def_list_block | blockquote_block | figure_block ) ;
top_level_block= ( meta_block | header_block | text_block | list_block | code_block | table_block | directive_block | extended_block | def_list_block | blockquote_block | figure_block | blank_line ) ;

(* ---- Core Block Types ---- *)

meta_block     = (META_TOKEN | META_ALIAS), meta_item, { ',', meta_item }, NEWLINE ;
meta_item      = IDENTIFIER, '=', (STRING | NUMBER | IDENTIFIER) ;

header_block   = (HEADER_TOKEN | HEADER_ALIAS), [ inline_content ], NEWLINE ;

text_block     = (TEXT_TOKEN | TEXT_ALIAS), ( inline_content | multi_line_text_block ), NEWLINE ;

list_block     = (LIST_TOKEN | LIST_ALIAS), NEWLINE, { INDENT, list_item } ;
list_item      = ( UNORDERED_MARKER | ORDERED_MARKER ), inline_content, NEWLINE, { indented_block } ;

code_block     = (CODE_TOKEN | CODE_ALIAS), [ language_specifier ], NEWLINE, code_content ;
language_specifier = IDENTIFIER ; (* e.g., python, javascript *)
code_content   = { INDENT, TEXT_LINE, NEWLINE } ; (* Assuming pre-processor handles extraction *)

table_block    = (TABLE_TOKEN | TABLE_ALIAS), NEWLINE, { INDENT, table_row_item } ;
table_row_item = '-', 'row:', inline_content, NEWLINE ;

def_list_block = (DEFLIST_TOKEN | DEFLIST_ALIAS), NEWLINE, { INDENT, ( def_term | def_description ) } ;
def_term       = (DEFLIST_TERM_TOKEN | DEFLIST_TERM_ALIAS), inline_content, NEWLINE ;
def_description= (DEFLIST_DESC_TOKEN | DEFLIST_DESC_ALIAS), inline_content, NEWLINE, { indented_block } ; (* Allow nested blocks in description *)

blockquote_block= (BLOCKQUOTE_TOKEN | BLOCKQUOTE_ALIAS), NEWLINE, { indented_block } ; (* Contains nested blocks *)

figure_block   = (FIGURE_TOKEN | FIGURE_ALIAS), NEWLINE, { INDENT, ( figure_src | figure_caption ) } ;
figure_src     = (FIGURE_SRC_TOKEN | FIGURE_SRC_ALIAS), inline_content, NEWLINE ; (* Expects URL/path *)
figure_caption = (FIGURE_CAPTION_TOKEN | FIGURE_CAPTION_ALIAS), inline_content, NEWLINE, { indented_block } ; (* Allow nested blocks for caption *)

directive_block = 'x-', IDENTIFIER, ':', [ inline_content ], NEWLINE, { indented_block } ;

extended_block = ( note_block | warn_block );
note_block     = (NOTE_TOKEN | NOTE_ALIAS), inline_content, NEWLINE ;
warn_block     = (WARN_TOKEN | WARN_ALIAS), inline_content, NEWLINE ;

(* ---- Content Elements ---- *)

inline_content = { content_element } ;
content_element= TEXT | inline_annotation | style_element | escape_sequence | inline_kv ;

inline_annotation = ( '(', annotation_content, ')' ) | ( '[', annotation_content, ']' ) ;
annotation_content = inline_content ; (* Allow full inline content within annotations *)

inline_kv      = '{', kv_pair, { ',', kv_pair }, '}' ;
kv_pair        = IDENTIFIER, ':', (STRING | IDENTIFIER | NUMBER) ;

(* --- Style Elements (e.g., @b(...) ) --- *)
style_element  = bold_style | italic_style | code_style | link_style ;

bold_style     = (BOLD_TOKEN | BOLD_ALIAS), '(', inline_content, ')' ; 
italic_style   = (ITALIC_TOKEN | ITALIC_ALIAS), '(', inline_content, ')' ;
code_style     = (CODE_TOKEN | CODE_ALIAS), '(', inline_content, ')' ;
link_style     = (LINK_TOKEN | LINK_ALIAS), '(', link_text, ',', link_url, [ ',', link_title ], ')' ;

link_text      = inline_content ; (* Text displayed for the link *)
link_url       = inline_content ; (* URL target *)
link_title     = inline_content ; (* Optional title attribute *)

multi_line_text_block = NEWLINE, INDENT, '>>>', NEWLINE, { TEXT_LINE, NEWLINE }, INDENT, '<<<';

escape_sequence= '\\', CHARACTER ; (* Handle escaped characters like \\, \#, etc. *)

(* ---- Basic Terminals ---- *)

blank_line     = { WHITESPACE }, NEWLINE ;

(* Note: Assumes lexer provides these base tokens *)
IDENTIFIER     = ? A sequence of letters, numbers, underscores, hyphens, not starting with a number (e.g., [a-zA-Z_][a-zA-Z0-9_-]*) ? ;
STRING         = ? A sequence of characters, potentially quoted, representing a value ? ;
NUMBER         = ? A numeric literal (integer or float) ? ; (* Added NUMBER placeholder *)
TEXT           = ? A sequence of non-special characters within a line ? ;
TEXT_LINE      = ? Any sequence of characters terminated by NEWLINE ? ;
INDENT         = '  ' ;
NEWLINE        = ? Platform-specific newline character(s) (e.g., \n, \r\n) ? ;
WHITESPACE     = ? A space or tab character ? ;
CHARACTER      = ? Any single Unicode character ? ;

(* --- Block Tokens & Aliases --- *)
META_TOKEN           = ? 'meta:' ? ;
META_ALIAS           = ? 'm:' ? ;
HEADER_TOKEN         = ? 'header:' ? ;
HEADER_ALIAS         = ? 'h:' ? ;
TEXT_TOKEN           = ? 'text:' ? ;
TEXT_ALIAS           = ? 't:' ? ;
LIST_TOKEN           = ? 'list:' ? ;
LIST_ALIAS           = ? 'l:' ? ;
CODE_TOKEN           = ? 'code:' ? ;
CODE_ALIAS           = ? 'c:' ? ;
TABLE_TOKEN          = ? 'table:' ? ;
TABLE_ALIAS          = ? 'tb:' ? ; (* Spec says tb:, token schema says tbl: - using tb: per spec *)
DEFLIST_TOKEN        = ? 'dl:' ? ;
DEFLIST_ALIAS        = ? 'dl' ? ;
DEFLIST_TERM_TOKEN   = ? 'dt:' ? ;
DEFLIST_TERM_ALIAS   = ? 'dt' ? ;
DEFLIST_DESC_TOKEN   = ? 'dd:' ? ;
DEFLIST_DESC_ALIAS   = ? 'dd' ? ;
BLOCKQUOTE_TOKEN     = ? 'bq:' ? ;
BLOCKQUOTE_ALIAS     = ? 'bq:' ? ; (* Alias same as token *)
FIGURE_TOKEN         = ? 'fig:' ? ;
FIGURE_ALIAS         = ? 'fig:' ? ; (* Alias same as token *)
FIGURE_SRC_TOKEN     = ? 'src:' ? ;
FIGURE_SRC_ALIAS     = ? '' ? ; (* No alias defined *) 
FIGURE_CAPTION_TOKEN = ? 'caption:' ? ;
FIGURE_CAPTION_ALIAS = ? '' ? ; (* No alias defined *) 
NOTE_TOKEN           = ? 'note:' ? ;
NOTE_ALIAS           = ? 'n:' ? ;
WARN_TOKEN           = ? 'warn:' ? ;
WARN_ALIAS           = ? 'w:' ? ;

(* --- List Item Markers --- *)
UNORDERED_MARKER     = ? '-' followed by WHITESPACE ? ;
ORDERED_MARKER       = ? (NUMBER | LETTER), '.', WHITESPACE ? ; (* e.g., '1. ', 'a. ' *)

(* --- Style Tokens & Aliases --- *)
BOLD_TOKEN     = ? '@b' ? ;
BOLD_ALIAS     = ? '@bold' ? ;
ITALIC_TOKEN   = ? '@i' ? ;
ITALIC_ALIAS   = ? '@italic' ? ;
CODE_TOKEN     = ? '@c' ? ;
CODE_ALIAS     = ? '@code' ? ;
LINK_TOKEN     = ? '@l' ? ;
LINK_ALIAS     = ? '@link' ? ;

COMMENT        = '#', { CHARACTER }, NEWLINE ; 