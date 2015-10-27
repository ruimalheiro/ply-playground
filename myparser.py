# Rui Malheiro    200901566
# Claudia Pereira 200801943

import sys
import ply.yacc as yacc
from myast import *

class MyParser:
	"""Parser.

    This class represents the parser and builds the abstract syntax tree.

    Attributes:
        tokens     : List of tokens.
        tree       : Abstract Syntax Tree structure.
        tree_depth : This attribute is the current depth of the tree.
    """

	def p_program_empty(self, p):
		"""
		program : 
		"""

	def p_program_statements(self, p):
		"""
		program : statements
		"""

	def p_statements_command(self, p):
		"""
		statements : command
		"""

	def p_command_command(self, p):
		"""
		statements : statements command
		"""

	def p_command_assignment_expression(self, p):
		"""
		command : ID ASSIGN expression COLON
		"""
		assign_node = AssignmentNode()
		assign_node.set_node_label("ASSIGNMENT")
		assign_node.set_target_id("v_" + p[1])
		assign_node.set_tree_depth(self.get_tree_depth())
		assign_node.set_parent(self.tree.get_current_node())

		self.tree.get_current_node().add_child(assign_node)

		expression_node = ExpressionNode()
		expression_node.set_node_label("EXPRESSION")
		expression_node.set_tree_depth(self.get_tree_depth())
		expression_node.set_parent(assign_node)
		expression_node.set_expression_tree_root_node(p[3])

		expression_node.build_expression_stack()

		assign_node.add_child(expression_node)
		assign_node.set_expression_type(expression_node.get_expression_type())
		assign_node.get_parent().add_symbol("v_" + p[1], expression_node.get_expression_type())

	def p_command_if_start(self, p):
		"""
		if_start : IF
		"""
		ifnode = IfNode()
		ifnode.set_node_label("IF")
		ifnode.set_tree_depth(self.get_tree_depth())
		ifnode.set_parent(self.tree.get_current_node())

		self.tree.get_current_node().add_child(ifnode)

		self.tree.set_current_node(ifnode)

	def p_command_if_expression(self, p):
		"""
		if_expression : expression
		"""
		if_expression_node = ExpressionNode()
		if_expression_node.set_node_label("IF_EXPRESSION")
		if_expression_node.set_tree_depth(self.get_tree_depth())
		if_expression_node.set_parent(self.tree.get_current_node())
		if_expression_node.set_expression_tree_root_node(p[1])

		if_expression_node.build_expression_stack()

		self.tree.get_current_node().add_child(if_expression_node)
		self.tree.get_current_node().set_expression_type(if_expression_node.get_expression_type())

	def p_command_if_then_begin(self, p):
		"""
		if_then_begin : THEN BEGIN
		"""
		then_node = ThenNode()
		then_node.set_node_label("THEN")
		then_node.set_tree_depth(self.get_tree_depth())
		then_node.set_parent(self.tree.get_current_node())

		self.tree.get_current_node().add_child(then_node)

		self.tree.set_current_node(then_node)

		self.increase_tree_depth()

	def p_command_if_else_begin(self, p):
		"""
		if_else_begin : ELSE BEGIN
		"""
		else_node = ElseNode()
		else_node.set_node_label("ELSE")
		else_node.set_tree_depth(self.get_tree_depth()-1)
		else_node.set_parent(self.tree.get_current_node().get_parent())

		self.tree.get_current_node().get_parent().add_child(else_node)

		self.tree.set_current_node(else_node)

	def p_command_if_statement(self, p):
		"""
		command : if_start if_expression if_then_begin statements END COLON
		"""
		self.decrease_tree_depth()

		self.tree.set_current_node(self.tree.get_current_node().get_parent().get_parent())

	def p_command_if_then_else_statement(self, p):
		"""
		command : if_start if_expression if_then_begin statements END if_else_begin statements END COLON
		"""
		self.decrease_tree_depth()

		self.tree.set_current_node(self.tree.get_current_node().get_parent().get_parent())

	def p_command_while_start(self, p):
		"""
		while_start : WHILE
		"""
		whilenode = WhileNode()
		whilenode.set_node_label("WHILE")
		whilenode.set_tree_depth(self.get_tree_depth())
		whilenode.set_parent(self.tree.get_current_node())

		self.tree.get_current_node().add_child(whilenode)

		self.tree.set_current_node(whilenode)

	def p_command_while_expression(self, p):
		"""
		while_expression : expression
		"""
		while_expression_node = ExpressionNode()
		while_expression_node.set_node_label("WHILE_EXPRESSION")
		while_expression_node.set_tree_depth(self.get_tree_depth())
		while_expression_node.set_parent(self.tree.get_current_node())
		while_expression_node.set_expression_tree_root_node(p[1])

		while_expression_node.build_expression_stack()

		self.tree.get_current_node().add_child(while_expression_node)
		self.tree.get_current_node().set_expression_type(while_expression_node.get_expression_type())

	def p_command_while_body(self, p):
		"""
		while_body : DO statements DONE COLON
		"""
		self.increase_tree_depth()

	def p_command_while_statement(self, p):
		"""
		command : while_start while_expression while_body
		"""
		self.decrease_tree_depth()

		self.tree.set_current_node(self.tree.get_current_node().get_parent())

	def p_expression_equality_comparison(self, p):
		"""
		expression : expression relational_equality_comparison_operation comparison
		"""
		operation_node = OperationNode()
		operation_node.set_operation(p[2])
		operation_node.add_child(p[1])
		operation_node.add_child(p[3])
		p[0] = operation_node

	def p_expression_comparison(self, p):
		"""
		expression : comparison
		"""
		p[0] = p[1]

	def p_comparison_arithmetic_expression_operations(self, p):
		"""
		comparison : comparison relational_inequality_comparison_operation arithmetic_expression
		"""
		operation_node = OperationNode()
		operation_node.set_operation(p[2])
		operation_node.add_child(p[1])
		operation_node.add_child(p[3])
		p[0] = operation_node

	def p_comparison_arithmetic_expression(self, p):
		"""
		comparison : arithmetic_expression
		"""
		p[0] = p[1]

	def p_arithmetic_expression_arithmetic_operation(self, p):
		"""
		arithmetic_expression : arithmetic_expression plus_minus_arithmetic_operation expression_term
		"""
		operation_node = OperationNode()
		operation_node.set_operation(p[2])
		operation_node.add_child(p[1])
		operation_node.add_child(p[3])
		p[0] = operation_node

	def p_arithmetic_expression_expression_term(self, p):
		"""
		arithmetic_expression : expression_term
		"""
		p[0] = p[1]

	def p_expression_term_arithmetic_operation(self, p):
		"""
		expression_term : expression_term times_divide_arithmetic_operation factor
		"""
		operation_node = OperationNode()
		operation_node.set_operation(p[2])
		operation_node.add_child(p[1])
		operation_node.add_child(p[3])
		p[0] = operation_node

	def p_expression_term_factor(self, p):
		"""
		expression_term : factor
		"""
		p[0] = p[1]

	def p_factor_expression_parenthesis(self, p):
		"""
		factor : LPAREN expression RPAREN
		"""
		p[0] = p[2]

	def p_factor_id(self, p):
		"""
		factor : ID
		"""
		number_node = NumberNode()
		number_node.set_value("v_" + p[1])
		p[0] = number_node

		if not self.tree.get_current_node().check_symbol("v_" + p[1]):
			print "Variable %s is not defined." %(p[1])
			self.tree.print_symbol_table()
			sys.exit()

		number_node.set_is_var(True)
		number_node.set_value_type(self.tree.get_current_node().get_symbol_type("v_" + p[1]))

	def p_factor_id_signed(self, p):
		"""
		factor : plus_minus_arithmetic_operation ID
		       | times_divide_arithmetic_operation ID  
		"""
		number_node = NumberNode()
		number_node.set_value("v_" + p[2])
		number_node.set_sign(p[1])
		p[0] = number_node

		if not self.tree.get_current_node().check_symbol("v_" + p[2]):
			print "Variable %s is not defined." %(p[2])
			self.tree.print_symbol_table()
			sys.exit()

		number_node.set_is_var(True)
		number_node.set_value_type(self.tree.get_current_node().get_symbol_type("v_" + p[2]))

	def p_factor_integer(self, p):
		"""
		factor : INTEGER
		"""
		number_node = NumberNode()
		number_node.set_value(p[1])
		number_node.set_value_type("INTEGER")
		p[0] = number_node

	def p_factor_integer_signed(self, p):
		"""
		factor : plus_minus_arithmetic_operation INTEGER
			   | times_divide_arithmetic_operation INTEGER
		"""
		number_node = NumberNode()
		number_node.set_value(p[2])
		number_node.set_value_type("INTEGER")
		number_node.set_sign(p[1])
		p[0] = number_node

	def p_factor_real(self, p):
		"""
		factor : REAL
		"""
		number_node = NumberNode()
		number_node.set_value(p[1])
		number_node.set_value_type("REAL")
		p[0] = number_node

	def p_factor_real_signed(self, p):
		"""
		factor : plus_minus_arithmetic_operation REAL
		       | times_divide_arithmetic_operation REAL
		"""
		number_node = NumberNode()
		number_node.set_value(p[2])
		number_node.set_value_type("REAL")
		number_node.set_sign(p[1])
		p[0] = number_node

	def p_plus_minus_arithmetic_operation(self, p):
		"""
		plus_minus_arithmetic_operation : PLUS
				  			            | MINUS
		"""
		p[0] = p[1]

	def p_times_divide_arithmetic_operation(self, p):
		"""
		times_divide_arithmetic_operation : TIMES
										  | DIVIDE
		"""
		p[0] = p[1]

	def p_relational_equality_comparison_operation(self ,p):
		"""
		relational_equality_comparison_operation : EQUAL
		                                         | NEQUAL
		"""
		p[0] = p[1]

	def p_relational_inequality_comparison_operation(self, p):
		"""
		relational_inequality_comparison_operation : LEQUAL
		                     					   | GEQUAL
		                                           | LTHEN
		                                           | GTHEN
		"""
		p[0] = p[1]

	def p_command_print(self, p):
		"""
		command : PRINT expression COLON
		"""
		print_node = PrintNode()
		print_node.set_node_label("PRINT")
		print_node.set_tree_depth(self.get_tree_depth())
		print_node.set_parent(self.tree.get_current_node())

		self.tree.get_current_node().add_child(print_node)

		expression_node = ExpressionNode()
		expression_node.set_node_label("EXPRESSION")
		expression_node.set_tree_depth(self.get_tree_depth())
		expression_node.set_parent(print_node)
		expression_node.set_expression_tree_root_node(p[2])

		expression_node.build_expression_stack()

		print_node.add_child(expression_node)
		print_node.set_expression_type(expression_node.get_expression_type())

	def p_error(self, p):
	    print "\nFAILED TO PARSE\n"
	    if p != None:
		    print "Token type:          %s" %(str(p.type))
		    print "Value:               %s" %(str(p.value))
		    print "Current line number: %s" %(str(p.lineno))
		    print "Token position:      %s" %(str(p.lexpos))
	    sys.exit()

	def __init__(self, tokens):
		self.tokens = tokens

		self.tree_depth = 0
		self.tree = AbstractSyntaxTree()

		root = Node()
		root.set_node_label("ROOT")
		root.set_tree_depth(0)

		self.tree.set_root(root)
		self.tree.set_current_node(root)

	def build(self, **kwargs):
		self.parser = yacc.yacc(module=self, **kwargs)

	def parse(self, data, **kwargs):
		self.parser.parse(data, **kwargs)

	def increase_tree_depth(self, debug=False):
		if debug:
			print self.tree_depth
		self.tree_depth+=1

	def decrease_tree_depth(self, debug=False):
		if debug:
			print self.tree_depth
		self.tree_depth-=1

	def set_tree_depth(self, value):
		self.tree_depth = value

	def get_tree_depth(self):
		return self.tree_depth

	def set_abstract_syntax_tree(self, new_abstract_syntax_tree):
		self.tree = new_abstract_syntax_tree

	def get_abstract_syntax_tree(self):
		return self.tree

	def build_abstract_syntax_tree(self):
		self.tree.build_tree_pass_one()

	def print_abstract_syntax_tree(self, print_tree=False):
		if print_tree:
			self.tree.print_tree()