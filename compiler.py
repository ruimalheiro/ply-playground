import sys
from mylexer import MyLexer
from myparser import MyParser
from mytact import ThreeAddressCodeTree
from mymips import MipsGenerator

# List of tokens.
tokens = [

		# Variables.
		'ID',

		# Numbers.
		'INTEGER',
		'REAL',
		
		# Arithmetic operators.
		'PLUS',
		'MINUS',
		'TIMES',
		'DIVIDE',

		# Relational operators.
		'EQUAL',
		'LEQUAL',
		'GEQUAL',
		'NEQUAL',
		'LTHEN',
		'GTHEN',

		# Parenthesis.
		'LPAREN',
		'RPAREN',

		# Delimiters.
		'COLON',

		#Assignment
		'ASSIGN',

	]

# List of reserved words.
reserved = {

		'if'   : 'IF',
		'then' : 'THEN',
		'begin': 'BEGIN',
		'end'  : 'END',
		'else' : 'ELSE',
		'while': 'WHILE',
		'do'   : 'DO',
		'done' : 'DONE',
		'print': 'PRINT',

	}

# Adding the reserved words to the tokens list.
tokens += list(reserved.values())

# Program that is passed as input.(A text file with the language code).
input = open(sys.argv[1], "r").read()

print "\n"

# Building the lexer.
lexer = MyLexer(tokens, reserved)
lexer.build()
lexer.tokenize(input)
lexer.print_tokens(False)

# Building the parser.
parser = MyParser(tokens)
parser.build()
parser.parse(input, debug=0)
parser.build_abstract_syntax_tree()
parser.print_abstract_syntax_tree(False)

# Building the tac tree.
tactree = ThreeAddressCodeTree()
tactree.set_abstract_syntax_tree(parser.get_abstract_syntax_tree())
tactree.build_three_address_code_tree()
tactree.build_three_address_code_stack()
tactree.print_three_address_code_tree(False)

# Generating MIPS code.
mips_generator = MipsGenerator()
mips_generator.set_tac_tree(tactree.get_abstract_syntax_tree())
mips_generator.generate_mips()
mips_generator.generate_output_file()
mips_generator.print_generated_mips_instructions(False)


print "\n\nCompiled successfully!\n"