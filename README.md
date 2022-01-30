# LTL_Parser_Lite
## Linear temporal logic lexer, parser, and validator

A small set of python scripts meant to parse and validate Linear Temporal Logic. 
This is just a homework project, but I enjoyed making it. 

/scripts/ includes the various scripts required to make the validator work.
/paths/ includes the "scenarios" that will be matched against the predicate rules.
"equations.txt" includes the actual rules that will be verified. 

The accepted context-free language is in lexer.py, but you may need a bit of digging to see what each symbol and predicate
maps to logically. Most of it is intended to follow usual conventions: & would be "and"; | would be "or", "U" would be "Until", ~ would be "Not", and so on and so forth. 
