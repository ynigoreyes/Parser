from typing import List
from Scanner import Scanner
from InvalidTokenExpection import InvalidTokenExpection

class Parser:
	def __init__(self, content):
		tokens, tokenValues = Scanner.scan(content)
		self.tokens = tokens
		self.tokenValues = tokenValues
		self.currentTokenPosition = 0
	   
	def parse(self): 
		self.program(0)
	
	def program(self, indent: int):
		self.print_xml('<program>', indent)
		self.stmt_list(indent + 1)
		self.print_xml('</program>', indent)

	def stmt_list(self, indent: int):
		self.print_xml('<stmt_list>', indent)
		# If there is still something left to read
		if self.currentTokenPosition < len(self.tokenValues):
			self.stmt(indent + 1)
			self.stmt_list(indent + 1)
		self.print_xml('</stmt_list>', indent)

	def stmt(self, indent: int):
		self.print_xml('<stmt>', indent)
		# If the next token is an id
		if self.match('id'):
			self.print_xml('<id>', indent + 1)
			self.print_xml(self.tokenValues[self.currentTokenPosition], indent + 2)
			self.print_xml('</id>', indent + 1)
			# Next one should be an assign
			self.currentTokenPosition += 1
			if self.match('assign'):
				self.print_xml('<assign>', indent + 1)
				self.print_xml(self.tokenValues[self.currentTokenPosition], indent + 2)
				self.print_xml('</assign>', indent + 1)
				self.currentTokenPosition += 1
			else:
				raise InvalidTokenExpection()
			self.expr(indent + 1)

		elif self.match('read'):
			self.print_xml('<read>', indent + 1)
			self.print_xml(self.tokenValues[self.currentTokenPosition], indent + 2)
			self.print_xml('</read>', indent + 1)
			self.currentTokenPosition += 1
			if self.match('id'):
				self.print_xml('<id>', indent + 1)
				self.print_xml(self.tokenValues[self.currentTokenPosition], indent + 2)
				self.print_xml('</id>', indent + 1)
				self.currentTokenPosition += 1
			else:
				raise InvalidTokenExpection()

		elif self.match('write'):
			self.print_xml('<write>', indent + 1)
			self.print_xml('write', indent + 2)
			self.print_xml('<write>', indent + 1)
			self.currentTokenPosition += 1
			self.expr(indent)
		
		else:
			raise InvalidTokenExpection()

		self.print_xml('</stmt>', indent)

	def expr(self, indent):
		self.print_xml('<expr>', indent)
		self.term(indent + 1)
		self.term_tail(indent + 1)
		self.print_xml('</expr>', indent)

	def term(self, indent: int):

		self.print_xml('<term>', indent)
		self.factor(indent + 1)
		self.fact_tail(indent + 1)
		self.print_xml('</term>', indent)
		return True

	def term_tail(self, indent: int):

		self.print_xml('<term_tail>', indent)

		if self.add_op(indent + 1):
			if self.term(indent + 1):
				self.term_tail(indent + 1)
			else:
				raise InvalidTokenExpection()
			
		self.print_xml('</term_tail>', indent)
		

	def factor(self, indent: int):
		if self.match('lparen'):
			self.print_xml('<lparen>', indent)
			self.print_xml('(', indent + 1)
			self.print_xml('</lparen>', indent)
			self.currentTokenPosition += 1
			self.expr(indent + 1)
			if self.match('rparen'):
				self.print_xml('<rparen>', indent)
				self.print_xml(')', indent + 1)
				self.print_xml('</rparen>', indent)
				self.currentTokenPosition += 1
				return True
			else:
				raise InvalidTokenExpection

		elif self.match('id'):
			self.print_xml('<id>', indent)
			self.print_xml(self.tokenValues[self.currentTokenPosition], indent + 1)
			self.currentTokenPosition += 1
			self.print_xml('</id>', indent)
			return True

		elif self.match('number'):
			self.print_xml('<number>', indent)
			self.print_xml(self.tokenValues[self.currentTokenPosition], indent + 1)
			self.currentTokenPosition += 1
			self.print_xml('</number>', indent)
			return True

		return False

	def fact_tail(self, indent: int):
		self.print_xml('<fact_tail>', indent)
		if self.mult_op(indent + 1):
			if self.factor(indent + 1):
				self.fact_tail(indent + 1)
			else:
				raise InvalidTokenExpection
		self.print_xml('</fact_tail>', indent)

	def add_op(self, indent: int):
		if self.match('plus'):
			self.print_xml('<plus>', indent)
			self.print_xml('+', indent + 1)
			self.currentTokenPosition += 1
			self.print_xml('</plus>', indent)
			return True
		
		elif self.match('minus'):
			self.print_xml('<minus>', indent)
			self.print_xml('-', indent + 1)
			self.currentTokenPosition += 1
			self.print_xml('</minus>', indent)
			return True

		return False

	def mult_op(self, indent):
		if self.match('mult'):
			self.print_xml('<times>', indent)
			self.print_xml('*', indent + 1)
			self.currentTokenPosition += 1
			self.print_xml('</times>', indent)
			return True

		elif self.match('div'):
			self.print_xml('<div>', indent)
			self.print_xml('/', indent + 1)
			self.currentTokenPosition += 1
			self.print_xml('</div>', indent)
			return True
		
		return False

	# Returns true if the next value matches the value provided
	def match(self, value):
		# If we are about to look ahead into out of bounds for the array, return false
		try:
			return self.tokens[self.currentTokenPosition] == value
		except:
			return False


	def print_xml(self, value, indent: int):
		print(indent * '\t' + value)
