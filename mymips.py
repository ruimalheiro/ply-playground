import sys
from myast import *
from mytact import *

class MipsGenerator:
	"""Generates MIPS code.

    This class processes the TAC structure and generates MIPS code.

    Attributes:
        tac_tree                      : A pointer to TAC tree structure.
        mapped_symbols                : A list that will contain the mapping of a register, to a symbol.
        used_integer_save_registers   : A list that will contain the used s* registers.
        used_float_registers          : A list that will contain the used f* registers.
        data_section_instructions     : A list containing the instructions to print in .data section.
        text_section_instructions     : A list containing the instructions to print in .text section.
        used_float_expression_labels  : A list that will contain the used FL* labels. These are used in expressions.
        new_tac_stack                 : A representations of the TAC code after replacing variables and other registers.
    """

	def __init__(self, tac_tree=None, mapped_symbols=[], used_integer_save_registers=[], used_float_registers=[], data_section_instructions=[], text_section_instructions=[], used_float_expression_labels=[], new_tac_stack=[]):
		self.tac_tree = tac_tree
		self.mapped_symbols = mapped_symbols
		self.used_integer_save_registers = used_integer_save_registers
		self.used_float_registers = used_float_registers
		self.data_section_instructions = data_section_instructions
		self.text_section_instructions = text_section_instructions
		self.used_float_expression_labels = used_float_expression_labels
		self.new_tac_stack = new_tac_stack

	def set_tac_tree(self, new_tac_tree):
		self.tac_tree = new_tac_tree

	def get_tac_tree(self):
		return self.tac_tree

	def set_mapped_symbols_list(self, new_mapped_symbols_list):
		self.mapped_symbols = new_mapped_symbols_list

	def get_mapped_symbols_list(self):
		return self.mapped_symbols

	def map_symbol_to_register(self, symbol, expression_type):
		"""Checks for a symbol mapping. If it doesn't exist, a new entry is created according to the expression type."""
		for mapping in self.mapped_symbols:
			if mapping[0] == symbol:
				return

		register = None
		if expression_type == "INTEGER":
			register = self.generate_integer_save_register()
			self.used_integer_save_registers.append(register)
		else:
			register = self.generate_float_register()
			self.used_float_registers.append(register)
		self.mapped_symbols.append([symbol, register, expression_type])

	def get_register_mapped_to_symbol(self, symbol):
		"""Returns the register mapped to the symbol."""
		for mapping in self.mapped_symbols:
			if mapping[0] == symbol:
				return mapping[1]
		return False

	def set_used_integer_save_registers_list(self, new_used_integer_save_registers_list):
		self.used_integer_save_registers = new_used_integer_save_registers_list

	def get_used_integer_save_registers_list(self):
		return self.used_integer_save_registers

	def generate_integer_save_register(self):
		i = 0
		while ("$s" + str(i)) in self.used_integer_save_registers:
			if i==7:
				return ("$s" + str(i))		
			i += 1
		return ("$s" + str(i))

	def remove_integer_save_register(self, register):
		self.used_integer_save_registers.remove(register)

	def set_used_float_registers_list(self, new_used_float_registers_list):
		self.used_float_registers = new_used_float_registers_list

	def get_used_float_registers_list(self):
		return self.used_float_registers

	def generate_float_register(self):
		i = 20
		while ("$f" + str(i)) in self.used_float_registers:
			if i==32:
				return ("$f" + str(i))		
			i += 1
		return ("$f" + str(i))

	def set_new_tac_stack(self, new_tac_stack):
		self.new_tac_stack = new_tac_stack

	def get_new_tac_stack(self):
		return self.new_tac_stack

	def replace_variables(self, node):
		"""Replaces all occurences of variables in the TAC by valid registers."""
		for instruction in node.get_expression_tac():
			for i in range(len(instruction)):
				if i != 0:
					if instruction[i][0] == "v":
						instruction[i] = self.get_register_mapped_to_symbol(instruction[i])
				else:
					if instruction[i][0] == "v":
						self.map_symbol_to_register(instruction[i], node.get_expression_type())
						instruction[i] = self.get_register_mapped_to_symbol(instruction[i])

	def replace_temporary_registers(self, node):
		"""Replaces temporary TAC registers by valid registers."""
		if node.get_expression_type() == "REAL":
			for instruction in node.get_expression_tac():
				for i in range(len(instruction)):
					if instruction[i][0] == "t":
						instruction[i] = "$f" + instruction[i][1]
		else:
			for instruction in node.get_expression_tac():
				for i in range(len(instruction)):
					if instruction[i][0] == "t":
						instruction[i] = "$t" + instruction[i][1]

	def generate_float_expression_label(self):
		i = 0
		while ("FL" + str(i) + ":") in self.used_float_expression_labels:		
			i += 1
		return ("FL" + str(i) + ":")

	def append_float_relational_operation(self, relop, instruction, operation):
		"""Handles the float expressions, that involve relational operators."""
		if relop == ">" or relop == ">=":
			self.text_section_instructions.append([operation, instruction[4], instruction[2]])
		else:
			self.text_section_instructions.append([operation, instruction[2], instruction[4]])

		label_then = self.generate_float_expression_label()
		self.used_float_expression_labels.append(label_then)
		label_else = self.generate_float_expression_label()
		self.used_float_expression_labels.append(label_else)

		if relop == "!=":
			self.text_section_instructions.append(["bc1t", label_else[:-1]])
			self.text_section_instructions.append(["lwc1", instruction[0], "FALSE"])
			self.text_section_instructions.append(["j", label_then[:-1]])
			self.text_section_instructions.append([label_else])
			self.text_section_instructions.append(["lwc1", instruction[0], "TRUE"])
			self.text_section_instructions.append([label_then])
		else:
			self.text_section_instructions.append(["bc1t", label_then[:-1]])
			self.text_section_instructions.append(["lwc1", instruction[0], "FALSE"])
			self.text_section_instructions.append(["j", label_else[:-1]])
			self.text_section_instructions.append([label_then])
			self.text_section_instructions.append(["lwc1", instruction[0], "TRUE"])
			self.text_section_instructions.append([label_else])

	def generate_assignment_if_while_mips(self, node):
		"""Generates the general MIPS code for the TAC contained in AssignmentNode, IfNode and WhileNode."""
		expression_type = node.get_expression_type()
		expression_tac = node.get_expression_tac()
		
		if expression_type == "INTEGER":
			for instruction in expression_tac:
				instruction_len = len(instruction)
				if instruction[0] == "if":
						self.text_section_instructions.append(["bge", instruction[1], "1", instruction[3][:-1]])
				else:
					if instruction_len == 1:
						self.text_section_instructions.append([instruction[0]])
					elif instruction_len == 2:
						self.text_section_instructions.append(["move", "$a0", instruction[1]])
						self.text_section_instructions.append(["li", "$v0", "1"])
						self.text_section_instructions.append(["syscall"])
						self.text_section_instructions.append(["li", "$v0", "4"])
						self.text_section_instructions.append(["la", "$a0", "newline"])
						self.text_section_instructions.append(["syscall"])
					elif  instruction_len == 3:
						self.text_section_instructions.append(["li", instruction[0], instruction[2]])
					elif instruction_len == 4:
						self.text_section_instructions.append(["li", instruction[0], instruction[2]+instruction[3]])
					else:
						if instruction[3] == "+":
							self.text_section_instructions.append(["add", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "-":
							self.text_section_instructions.append(["sub", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "*":
							self.text_section_instructions.append(["mul", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "/":
							self.text_section_instructions.append(["div", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "==":
							self.text_section_instructions.append(["seq", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "!=":
							self.text_section_instructions.append(["sne", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == ">":
							self.text_section_instructions.append(["sgt", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "<":
							self.text_section_instructions.append(["slt", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == ">=":
							self.text_section_instructions.append(["sge", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "<=":
							self.text_section_instructions.append(["sle", instruction[0], instruction[2], instruction[4]])
		else:
			for instruction in expression_tac:
				instruction_len = len(instruction)
				if instruction[0] == "if":
						self.text_section_instructions.append(["lwc1", "$f11", "TRUE"])
						self.text_section_instructions.append(["c.le.s", "$f11", instruction[1]])
						self.text_section_instructions.append(["bc1t", instruction[3][:-1]])
				else:
					if instruction_len == 1:
						self.text_section_instructions.append([instruction[0]])
					elif instruction_len == 2:
						self.text_section_instructions.append(["mov.s", "$f12", instruction[1]])
						self.text_section_instructions.append(["li", "$v0", "2"])
						self.text_section_instructions.append(["syscall"])
						self.text_section_instructions.append(["li", "$v0", "4"])
						self.text_section_instructions.append(["la", "$a0", "newline"])
						self.text_section_instructions.append(["syscall"])
					elif  instruction_len == 3:
						float_data = self.generate_float_expression_label()
						self.used_float_expression_labels.append(float_data)
						self.data_section_instructions.append([float_data, ".float", instruction[2]])
						self.text_section_instructions.append(["lwc1", instruction[0], float_data[:-1]])
					elif instruction_len == 4:
						float_data = self.generate_float_expression_label()
						self.used_float_expression_labels.append(float_data)
						self.data_section_instructions.append([float_data, ".float", instruction[2]+instruction[3]])
						self.text_section_instructions.append(["lwc1", instruction[0], float_data[:-1]])
					else:
						if instruction[3] == "+":
							self.text_section_instructions.append(["add.s", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "-":
							self.text_section_instructions.append(["sub.s", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "*":
							self.text_section_instructions.append(["mul.s", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "/":
							self.text_section_instructions.append(["div.s", instruction[0], instruction[2], instruction[4]])
						elif instruction[3] == "==":
							self.append_float_relational_operation("==", instruction, "c.eq.s")
						elif instruction[3] == "!=":
							self.append_float_relational_operation("!=", instruction, "c.eq.s")
						elif instruction[3] == ">":
							self.append_float_relational_operation(">", instruction, "c.lt.s")
						elif instruction[3] == "<":
							self.append_float_relational_operation("<", instruction, "c.lt.s")
						elif instruction[3] == ">=":
							self.append_float_relational_operation(">=", instruction, "c.le.s")
						elif instruction[3] == "<=":
							self.append_float_relational_operation("<=", instruction, "c.le.s")

	def generate_labels_mips(self, node):
		for instruction in node.get_expression_tac():
			instruction_len = len(instruction)
			if instruction_len == 1:
				self.text_section_instructions.append([instruction[0]])
			elif instruction_len == 2:
				self.text_section_instructions.append(["j", instruction[1][:-1]])

	def build_new_tac_stack(self, node):
		for instruction in node.get_expression_tac():
			result_string = ""
			for element in instruction:
				result_string += str(element) + " "
			self.new_tac_stack.append(result_string)

	def generate_mips(self):
		root = self.tac_tree.get_root()

		node_list = []
		node_list.append(root)

		self.data_section_instructions.append([".data"])
		self.data_section_instructions.append(["newline: .asciiz \"\\n\""])
		self.data_section_instructions.append(["FALSE: .float 0.0"])
		self.data_section_instructions.append(["TRUE: .float 1.0"])

		while len(node_list) != 0:

			node = node_list.pop(len(node_list)-1)

			if isinstance(node, AssignmentNode) or isinstance(node, IfNode) or isinstance(node, WhileNode) or isinstance(node, PrintNode):
				self.replace_variables(node)
				self.replace_temporary_registers(node)
				self.build_new_tac_stack(node)
				self.generate_assignment_if_while_mips(node);

			if isinstance(node, LabelNode):
				self.generate_labels_mips(node)
				self.build_new_tac_stack(node)

			for child_node in node.get_children_list():
				node_list.append(child_node)

		self.text_section_instructions.append(["li $v0, 10"])
		self.text_section_instructions.append(["syscall"])

	def generate_output_file(self):
		f = open("output.asm", "w")

		for instruction in self.data_section_instructions:
			result_string = ""
			for element in instruction:
				result_string += str(element) + " "
			f.write(result_string + "\n")

		f.write(".text\n")

		for instruction in self.text_section_instructions:
			result_string = ""
			for element in instruction:
				result_string += str(element) + " "
			f.write(result_string + "\n")

		f.close()

	def print_generated_mips_instructions(self, print_tree=False):
		if print_tree:
			print "\nNew TAC:\n\n"
			for instruction in self.new_tac_stack:
				print instruction

			print "\n"
			print "MIPS:\n"

			for instruction in self.data_section_instructions:
				result_string = ""
				for element in instruction:
					result_string += str(element) + " "
				print result_string

			for instruction in self.text_section_instructions:
				result_string = ""
				for element in instruction:
					result_string += str(element) + " "
				print result_string

			print "\n"
			print self.mapped_symbols