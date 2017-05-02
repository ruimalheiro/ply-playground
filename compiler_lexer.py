import sys
import ply.lex as lex

class CompilerLexer:
  """Lexer.

    This class represents the lexer used in the compiler and defines the tokens and reserved words.

    Attributes:
        tokens   : List of tokens.
        reserved : List of reserved words.
        t_*      : Token expression to match.
    """

  t_INTEGER = r'\d+'
  t_REAL    = r'\d+\.\d+'
  t_PLUS    = r'\+'
  t_MINUS   = r'-'
  t_TIMES   = r'\*'
  t_DIVIDE  = r'/'
  t_LPAREN  = r'\('
  t_RPAREN  = r'\)'
  t_COLON   = r';'

  t_EQUAL   = r'=='
  t_LEQUAL  = r'<='
  t_GEQUAL  = r'>='
  t_NEQUAL  = r'!='
  t_LTHEN   = r'<'
  t_GTHEN   = r'>'

  t_ASSIGN  = r'<-' 

  t_ignore  = ' \t'

  def __init__(self, tokens, reserved):
    self.tokens = tokens
    self.reserved = reserved

  def t_ID(self, t):
    # Checks if the ID is valid. We cannot create ID's with the same text as the reserved words.
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = self.reserved.get(t.value, "ID")
    return t

  def t_error(self, t):
    # Error handler.
    print "Invalid char: %s" % t.value[0]
    t.lexer.skip(1)

  def t_newline(self, t):
    # Defines a newline, so we can keep track of the line number.
    r'\n+'
    t.lexer.lineno += len(t.value)

  def build(self, **kwargs):
    """Builds the lexer with the respective kwargs."""
    self.lexer = lex.lex(module=self, **kwargs)

  def tokenize(self, data):
    """Reads the input and matches the symbols to the defined tokens."""
    self.lexer.input(data)

  def print_tokens(self, print_tokens=False):
    """Prints the list of tokens found."""
    if print_tokens:
      while True:
        token = self.lexer.token()
        if not token:
          break
        print token
