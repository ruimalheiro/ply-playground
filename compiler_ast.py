import sys

class Node:
	"""General Node definition.

    This class represents the general contents of nodes in the tree. All the other nodes will extend this class.

    Attributes:
        parent        : A pointer to the parent node.
        children_list : A list that will contain the children nodes.
        tree_depth    : The depth of this node in the tree.
        node_label    : An identification for this node.
        symbol_table  : A list containing all the symbols found in the current depth that are accessible for this node.
    """

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[]):
		self.parent = parent
		self.children_list = list(children_list)
		self.tree_depth = tree_depth
		self.node_label = node_label
		self.symbol_table = symbol_table

	def set_parent(self, new_node):
		self.parent = new_node

	def get_parent(self):
		return self.parent

	def get_number_of_children(self):
		return len(self.children_list)

	def add_child(self, node):
		self.children_list.append(node)

	def add_children_list(self, nodes):
		for node in nodes:
			self.children_list.append(node)

	def set_children_list(self, new_children_list):
		self.children_list = new_children_list

	def get_children_list(self):
		return self.children_list

	def set_tree_depth(self, new_index):
		self.tree_depth = new_index

	def get_tree_depth(self):
		return self.tree_depth

	def set_node_label(self, label):
		self.node_label = label

	def get_node_label(self):
		return self.node_label

	def set_symbol_table(self, new_symbol_table):
		self.symbol_table = new_symbol_table

	def get_symbol_table(self):
		return self.symbol_table

	def add_symbol(self, symbol, symbol_type):
		""" Checks if there is an occurrence of the same symbol but with a different type. If so, returns error.
		    Add the symbol to the symbol_table at the same node.
		"""
		node = self
		while node != None:
			for element in node.symbol_table:
				if element[0] == symbol:
					if element[1] != symbol_type:
						print "Type error. Variable %s was initialized as: %s" %(symbol[2:], element[1])
						sys.exit()
			node = node.get_parent()
		self.symbol_table.append([symbol, symbol_type, len(self.symbol_table)])

	def get_symbol_type(self, symbol):
		""" Checks if there is an occurrence of the same symbol but with a different type.
		    Returns symbol type if exists.
		"""
		node = self
		while node != None:
			for element in node.symbol_table:
				if element[0] == symbol:
					return element[1]
			node = node.get_parent()
		return False

	def check_symbol(self, symbol):
		""" Checks if the symbol exists in the symbol_table of the current node or above.
		"""
		node = self
		while node != None:
			for element in node.symbol_table:
				if element[0] == symbol:
					return True
			node = node.get_parent()
		return False


class ExpressionNode(Node):
	"""Represents an expression.

    This class holds the root to an expression tree and builds a string representation of the expression and a stack representation.
    It uses the stack to generate three address code.

    Attributes:
        expression_tree_root_node : A pointer to the root of the tree that represents the expression.
        expression_type           : The is the type of the expression, INTEGER or REAL.
        expression_stack          : This stack contains the expression ready to be processed so we can generate three address code.
        expression_string         : A string containing the representation of the expression stack.
        expression_tac            : The generated three address code.
    """

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], expression_tree_root_node=None, expression_type=None, expression_stack=None, expression_string=None, expression_tac=None):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.expression_tree_root_node = expression_tree_root_node
		self.expression_type = expression_type
		self.expression_stack = expression_stack
		self.expression_string = expression_string
		self.expression_tac = expression_tac

	def set_expression_tree_root_node(self, new_expression_tree_root_node):
		self.expression_tree_root_node = new_expression_tree_root_node

	def get_expression_tree_root_node(self):
		return self.expression_tree_root_node

	def set_expression_type(self, new_expression_type):
		self.expression_type = new_expression_type

	def get_expression_type(self):
		return self.expression_type

	def set_expression_stack(self, new_expression_stack):
		self.expression_stack = new_expression_stack

	def get_expression_stack(self):
		return self.expression_stack

	def set_expression_string(self, new_expression_string):
		self.expression_string = new_expression_string

	def get_expression_string(self):
		return self.expression_string

	def set_expression_tac(self, new_expression_tac):
		self.expression_tac = new_expression_tac

	def get_expression_tac(self):
		return self.expression_tac

	def build_expression_stack(self):
		"""Traverses the expression tree to build the stack in postfix representation."""
		node_list = []
		node_list.append(self.get_expression_tree_root_node())

		expression_stack = []
		expression_string = ""

		expression_type_test = []

		while len(node_list) != 0:
			node = node_list.pop(len(node_list)-1)

			if isinstance(node, NumberNode):
				expression_stack.append((node.get_value(), node))
				if not node.get_value_type() in expression_type_test:
					expression_type_test.append(node.get_value_type())

			if isinstance(node, OperationNode):
				expression_stack.append((node.get_operation(), node))

			for child_nodes in node.get_children_list():
				node_list.append(child_nodes)

		expression_stack.reverse()

		for e in expression_stack:
			expression_string += str(e[0])

		self.expression_stack = expression_stack
		self.expression_string = expression_string

		if len(expression_type_test) != 1:
			print "Different types in expression: %s" %(self.expression_string)
			print "Expressions must have all elements Integer or all elements Real."
			print expression_type_test
			sys.exit()

		self.set_expression_type(expression_type_test[0])


class AssignmentNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], target_id=None, expression_node=None, expression_type=None, expression_tac=None):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.target_id = target_id
		self.expression_node = expression_node
		self.expression_type =expression_type
		self.expression_tac = expression_tac

	def set_target_id(self, new_id):
		self.target_id = new_id

	def get_target_id(self):
		return self.target_id

	def set_expression_node(self, new_expression_node):
		self.expression_node = new_expression_node

	def get_expression_node(self):
		return self.expression_node

	def set_expression_type(self, new_expression_type):
		self.expression_type = new_expression_type

	def get_expression_type(self):
		return self.expression_type

	def set_expression_tac(self, new_expression_tac):
		self.expression_tac = new_expression_tac

	def get_expression_tac(self):
		return self.expression_tac


class IfNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], expression_type=None, expression_tac=None):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.expression_tac = expression_tac
		self.expression_type = expression_type

	def set_expression_type(self, new_expression_type):
		self.expression_type = new_expression_type

	def get_expression_type(self):
		return self.expression_type

	def set_expression_tac(self, new_expression_tac):
		self.expression_tac = new_expression_tac

	def get_expression_tac(self):
		return self.expression_tac


class ThenNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[]):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)


class ElseNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[]):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)


class WhileNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], expression_node=None, expression_type=None, expression_tac=None):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.expression_node = expression_node
		self.expression_tac = expression_tac
		self.expression_type = expression_type

	def set_expression_node(self, new_node):
		self.expression_node = new_node

	def get_expression_node(self):
		return self.expression_node

	def set_expression_type(self, new_expression_type):
		self.expression_type = new_expression_type

	def get_expression_type(self):
		return self.expression_type

	def set_expression_tac(self, new_expression_tac):
		self.expression_tac = new_expression_tac

	def get_expression_tac(self):
		return self.expression_tac


class OperationNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], operation=None):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.operation = operation

	def set_operation(self, new_operation):
		self.operation = new_operation

	def get_operation(self):
		return self.operation


class NumberNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], value=None, value_type=None, sign=None, is_var=False):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.value = value
		self.value_type = value_type
		self.sign = sign
		self.is_var = is_var

	def set_value(self, new_value):
		self.value = new_value

	def get_value(self):
		return self.value

	def set_value_type(self, new_value_type):
		self.value_type = new_value_type

	def get_value_type(self):
		return self.value_type

	def set_sign(self, new_sign):
		self.sign = new_sign

	def get_sign(self):
		return self.sign

	def set_is_var(self, is_var):
		self.is_var = is_var

	def is_var(self):
		return self.is_var


class PrintNode(Node):

	def __init__(self, parent=None, children_list=[], tree_depth=None, node_label=None, symbol_table=[], expression_type=None, expression_tac=None):
		Node.__init__(self, parent, children_list, tree_depth, node_label, symbol_table)
		self.expression_tac = expression_tac
		self.expression_type = expression_type

	def set_expression_type(self, new_expression_type):
		self.expression_type = new_expression_type

	def get_expression_type(self):
		return self.expression_type

	def set_expression_tac(self, new_expression_tac):
		self.expression_tac = new_expression_tac

	def get_expression_tac(self):
		return self.expression_tac


class AbstractSyntaxTree:
	"""The Abstract Syntax Tree.

    This class represents the AST. This tree will be used to generate TAC and MIPS.

    Attributes:
        root           : A pointer to the root of the tree.
        current_node   : A pointer to the current node. This is useful to build the tree while the parsing is being processed.
    """

	def __init__(self, root=None, current_node=None):
		self.root = root
		self.current_node = current_node

	def set_root(self, node):
		self.root = node

	def get_root(self):
		return self.root

	def set_current_node(self, node):
		self.current_node = node

	def get_current_node(self):
		return self.current_node

	def build_tree_pass_one(self):
		"""This fixes the order of the nodes in the tree for future traverses."""
		node_list = []
		node_list.append(self.get_root())

		while len(node_list) != 0:
			node = node_list.pop(len(node_list)-1)

			node.get_children_list().reverse()
			for child in node.get_children_list():
				node_list.append(child)

	def print_symbol_table(self):
		print "\n"
		print "Symbol table:\n"
		print self.current_node.get_symbol_table()

	def print_tree(self):
		node_list = []
		node_list.append(self.get_root())

		while len(node_list) != 0:
			node = node_list.pop(len(node_list)-1)

			space = ""
			for i in range(node.get_tree_depth()):
				space+="-"
			
			print "%s  %s%s" %( str(node.get_tree_depth()), str(space), str(node.get_node_label()) )

			if isinstance(node, ExpressionNode):
				space = "   "
				
				for i in range(node.get_tree_depth()):
					space += " "

				print "%sexpression stack:  %s" %(space, node.get_expression_string())
				print "%sexpression type:   %s" %(space, node.get_expression_type())

			for child in node.get_children_list():
				node_list.append(child)
