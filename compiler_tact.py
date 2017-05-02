import sys
from compiler_ast import *

class LabelNode:

  def __init__(self, label=None, children_list=[], expression_tac=None):
    self.label = label
    self.children_list = children_list
    self.expression_tac = expression_tac

  def set_label(self, new_label):
    self.label = new_label

  def get_label(self):
    return self.label

  def set_children_list(self, new_children_list):
    self.children_list = new_children_list

  def get_children_list(self):
    return self.children_list

  def set_expression_tac(self, new_expression_tac):
    self.expression_tac = new_expression_tac

  def get_expression_tac(self):
    return self.expression_tac

class ThreeAddressCodeTree:
  """Three address code tree structure.

    This class uses the abstract syntax tree and generates TAC.

    Attributes:
        abstract_syntax_tree : A pointer to the AST.
        used_registers       : A list that will contain the registers t* that are in use.
        used_labels          : A list that will contain the labels L* that are in use.
        three_address_stack  : This structure will cointain the representation of the input program in TAC.
    """

  def __init__(self, abstract_syntax_tree=None, used_registers=[], used_labels=[], three_address_stack=[]):
    self.abstract_syntax_tree = abstract_syntax_tree
    self.used_registers = used_registers
    self.used_labels = used_labels
    self.three_address_stack = three_address_stack

  def set_abstract_syntax_tree(self, abstract_syntax_tree):
    self.abstract_syntax_tree = abstract_syntax_tree

  def get_abstract_syntax_tree(self):
    return self.abstract_syntax_tree

  def set_used_registers_list(self, used_registers_list):
    self.used_registers = used_registers_list

  def get_used_registers_list(self):
    return self.used_registers

  def add_used_register(self, register):
    self.used_registers.append(register)

  def remove_used_register(self, register):
    if register in self.used_registers:
      self.used_registers.remove(register)

  def generate_register(self):
    """Generate valid registers t*."""
    i = 0
    r = "t"
    while (r + str(i)) in self.used_registers:
      i += 1
    return (r + str(i))

  def set_used_labels_list(self, new_used_label_list):
    self.used_labels = new_used_label_list

  def get_used_labels_list(self):
    return self.used_labels

  def set_three_address_stack(self, new_three_address_stack):
    self.three_address_stack = new_three_address_stack

  def get_three_address_stack(self):
    return self.three_address_stack

  def generate_label(self):
    """Generate valid labels L*."""
    i = 0
    while ("L" + str(i) + ":") in self.used_labels:
      i += 1
    self.used_labels.append(("L" + str(i) + ":"))
    return ("L" + str(i) + ":")

  def set_signed_value(self, element, register, stack):
    sign_number_node = NumberNode()
    sign_number_node.set_value(register)
    sign_number_node.set_sign(element[1].get_sign())
    sign_number_node.set_is_var(True)
    stack.append([str(register), "=", str(sign_number_node.get_sign()), str(element[0])])
    element[0] = str(register)
    element[1] = sign_number_node

  def set_unsigned_value(self, element,  register, stack):
    unsign_number_node = NumberNode()
    unsign_number_node.set_value(register)
    unsign_number_node.set_is_var(True)
    stack.append([str(register), "=", str(element[0])])
    element[0] = str(register)
    element[1] = unsign_number_node

  def compile_expression_stack(self, expression_stack):
    """Generates the TAC for an expression."""
    solution_stack = []
    instruction_stack = []

    is_small = False
    if len(expression_stack) <= 2:
      is_small = True

    while len(expression_stack) != 0:
      e = expression_stack.pop(0)

      result = None

      if isinstance(e[1], NumberNode):
        solution_stack.append([e[0], e[1]])

      if isinstance(e[1], OperationNode):
        x = solution_stack.pop(len(solution_stack)-1)
        y = solution_stack.pop(len(solution_stack)-1)

        op = e[0]

        register = None

        if x[1].is_var and y[1].is_var:
          self.remove_used_register(x[0])
          self.remove_used_register(y[0])
          register = self.generate_register()
          self.add_used_register(register)
        else:
          if x[1].is_var:
            self.remove_used_register(x[0])
          elif x[1].get_sign() != None:
            register = self.generate_register()
            self.add_used_register(register)
            self.set_signed_value(x, register, instruction_stack)
          else:
            register = self.generate_register()
            self.add_used_register(register)
            self.set_unsigned_value(x, register, instruction_stack)

          if y[1].is_var:
            self.remove_used_register(y[0])
          elif y[1].get_sign() != None:
            register = self.generate_register()
            self.add_used_register(register)
            self.set_signed_value(y, register, instruction_stack)
          else:
            register = self.generate_register()
            self.add_used_register(register)
            self.set_unsigned_value(y, register, instruction_stack)
        
        self.remove_used_register(x[0])
        self.remove_used_register(y[0])       
        self.add_used_register(register)

        if op == "+":
          result = [str(register), "=", str(y[0]), "+", str(x[0])] 
        if op == "-":
          result = [str(register), "=", str(y[0]), "-", str(x[0])] 
        if op == "*":
          result = [str(register), "=", str(y[0]), "*", str(x[0])]
        if op == "/":
          result = [str(register), "=", str(y[0]), "/", str(x[0])]
        if op == ">":
          result = [str(register), "=", str(y[0]), ">", str(x[0])]
        if op == "<":
          result = [str(register), "=", str(y[0]), "<", str(x[0])]
        if op == ">=":
          result = [str(register), "=", str(y[0]), ">=", str(x[0])]
        if op == "<=":
          result = [str(register), "=", str(y[0]), "<=", str(x[0])]
        if op == "==":
          result = [str(register), "=", str(y[0]), "==", str(x[0])]
        if op == "!=":
          result = [str(register), "=", str(y[0]), "!=", str(x[0])]

        instruction_stack.append(result)

        new_number_node = NumberNode()
        new_number_node.set_value(register)
        new_number_node.set_is_var(True)

        solution_stack.append((register, new_number_node))

    if is_small:
      x = solution_stack.pop(len(solution_stack)-1)
      if x[1].get_sign() != None:
        register = self.generate_register()
        self.add_used_register(register)
        instruction_stack.append([str(register), "=", str(x[1].get_sign()), str(x[0])])
      else:
        register = self.generate_register()
        self.add_used_register(register)
        instruction_stack.append([str(register), "=", str(x[0])])

    return instruction_stack

  def compile_and_set_expression_tac(self, node):
    for child in node.get_children_list():
      if isinstance(child, ExpressionNode):
        child.set_expression_tac(self.compile_expression_stack(child.get_expression_stack()))
        node.set_expression_tac(child.get_expression_tac())

  def build_three_address_code_tree(self):
    """This function builds the TAC for the different nodes."""
    root = self.abstract_syntax_tree.get_root()

    node_list = []
    node_list.append(root)
    while len(node_list) != 0:

      node = node_list.pop(len(node_list)-1)

      if isinstance(node, AssignmentNode):
        self.compile_and_set_expression_tac(node)

        self.remove_used_register(node.get_expression_tac()[len(node.get_expression_tac())-1][0])
        node.get_expression_tac()[len(node.get_expression_tac())-1][0] = node.get_target_id()

      if isinstance(node, IfNode):
        self.compile_and_set_expression_tac(node)

        if len(node.get_children_list()) == 3:
          node.get_children_list()[0], node.get_children_list()[1] = node.get_children_list()[1], node.get_children_list()[0] 

      if isinstance(node, ThenNode):
        then_label = self.generate_label()
        else_label = self.generate_label()

        then_label_node = LabelNode()
        then_label_node.set_label(then_label)
        then_label_node.set_expression_tac([[then_label]])

        goto_label_node = LabelNode()
        goto_label_node.set_label("goto " + else_label)
        goto_label_node.set_expression_tac([["goto", else_label]])

        else_label_node = LabelNode()
        else_label_node.set_label(else_label)
        else_label_node.set_expression_tac([[else_label]])

        node.get_children_list().append(then_label_node)
        node.get_children_list().append(goto_label_node)
        node.get_children_list().insert(0, else_label_node)

        self.remove_used_register(node.get_parent().get_expression_tac()[len(node.get_parent().get_expression_tac())-1][0])
        if len(node.get_parent().get_expression_tac()[len(node.get_parent().get_expression_tac())-1]) == 3:
          element = node.get_parent().get_expression_tac().pop(len(node.get_parent().get_expression_tac())-1)
          var = element[2]
        else:
          var = node.get_parent().get_expression_tac()[len(node.get_parent().get_expression_tac())-1][0]
        node.get_parent().get_expression_tac().append(["if", var, "goto", then_label])

      if isinstance(node, WhileNode):
        self.compile_and_set_expression_tac(node)

        goto_in_label = self.generate_label()
        goto_expression_label = self.generate_label()
        goto_out_label = self.generate_label()

        goto_out_label_node = LabelNode()
        goto_out_label_node.set_label("goto " + goto_out_label)
        goto_out_label_node.set_expression_tac([["goto", goto_out_label]])

        in_label_node = LabelNode()
        in_label_node.set_label(goto_in_label)
        in_label_node.set_expression_tac([[goto_in_label]])

        goto_expression_label_node = LabelNode()
        goto_expression_label_node.set_label("goto " + goto_expression_label)
        goto_expression_label_node.set_expression_tac([["goto", goto_expression_label]])

        out_label_node = LabelNode()
        out_label_node.set_label(goto_out_label)
        out_label_node.set_expression_tac([[goto_out_label]])

        node.get_expression_tac().insert(0, [goto_expression_label])

        node.get_children_list().append(in_label_node)
        node.get_children_list().append(goto_out_label_node)
        node.get_children_list().insert(0, goto_expression_label_node)
        node.get_children_list().insert(0, out_label_node)

        self.remove_used_register(node.get_expression_tac()[len(node.get_expression_tac())-1][0])
        if len(node.get_expression_tac()[len(node.get_expression_tac())-1]) == 3:
          element = node.get_expression_tac().pop(len(node.get_expression_tac())-1)
          var = element[2]
        else:
          var = node.get_expression_tac()[len(node.get_expression_tac())-1][0]
        node.get_expression_tac().append(["if", var, "goto", goto_in_label])

      if isinstance(node, PrintNode):
        self.compile_and_set_expression_tac(node)

        self.remove_used_register(node.get_expression_tac()[len(node.get_expression_tac())-1][0])
        if len(node.get_expression_tac()[len(node.get_expression_tac())-1]) == 3:
          element = node.get_expression_tac().pop(len(node.get_expression_tac())-1)
          var = element[2]
        else:
          var = node.get_expression_tac()[len(node.get_expression_tac())-1][0]
        node.get_expression_tac().append(["print", var])

      for child_node in node.get_children_list():
        node_list.append(child_node)

  def build_three_address_code_stack(self):
    """Prepares the TAC stack for the next step. Generate MIPS code."""
    root = self.abstract_syntax_tree.get_root()

    node_list = []
    node_list.append(root)

    while len(node_list) != 0:

      node = node_list.pop(len(node_list)-1)

      if isinstance(node, AssignmentNode) or isinstance(node, IfNode) or isinstance(node, WhileNode) or isinstance(node, LabelNode) or isinstance(node, PrintNode):
        self.get_three_address_stack().append(node.get_expression_tac())

      for child_node in node.get_children_list():
        node_list.append(child_node)

  def print_three_address_code_tree(self, print_tree=False):
    if print_tree:
      for instruction_list in self.get_three_address_stack():
        for instruction in instruction_list:
          result_string = ""
          for element in instruction:
            result_string += str(element) + " "
          print result_string

      print "\n"
      print "Temporary registers in use:"
      print self.get_used_registers_list()
      print "\n"


