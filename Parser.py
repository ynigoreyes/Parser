from typing import List
from Scanner import Scanner

class Parser:
	def __init__(self, a: List):
		self.s = Scanner(a)
		self.tokens = self.s.scan()
		self.tokenValues = self.s.list()
		self.currentTokenPosition = 0
	   
	def parse(self): 
		print('token list: {0}'.format(self.tokens[:]))
		print('token values list: {0}'.format(self.tokenValues[:]))
		self.program(0)
	
	def program(self, level: int):
		self.print_with_indent('<program>', level)
		self.stmt_list(level + 1)
		self.print_with_indent('</program>', level)

	def stmt_list(self, level: int):
		self.print_with_indent('<stmt_list>', level)
		# If there is still something left to read
		if self.currentTokenPosition < len(self.tokenValues):
			self.stmt(level + 1)
			self.stmt_list(level + 1)
		self.print_with_indent('</stmt_list>', level)

	def stmt(self, level: int):
		self.print_with_indent('<stmt>', level)
		# If the next token is an id
		if self.match('id'):
			self.print_with_indent('<id>', level + 1)
			self.print_with_indent(self.tokenValues[self.currentTokenPosition], level + 2)
			self.print_with_indent('</id>', level + 1)
			# Next one should be an assign
			self.currentTokenPosition += 1
			if self.match('assign'):
				self.print_with_indent('<assign>', level + 1)
				self.print_with_indent(self.tokenValues[self.currentTokenPosition], level + 2)
				self.print_with_indent('</assign>', level + 1)
				self.currentTokenPosition += 1
			else:
				raise Exception()
			self.expr(level)

		elif self.match('read'):
			self.print_with_indent('<read>', level + 1)
			self.print_with_indent(self.tokenValues[self.currentTokenPosition], level + 2)
			self.print_with_indent('</read>', level + 1)
			self.currentTokenPosition += 1
			if self.match('id'):
				self.print_with_indent('<id>', level + 1)
				self.print_with_indent(self.tokenValues[self.currentTokenPosition], level + 2)
				self.print_with_indent('</id>', level + 1)
				self.currentTokenPosition += 1
			else:
				raise Exception()

		elif self.match('write'):
			self.print_with_indent('<write>', level + 1)
			self.print_with_indent('write', level + 2)
			self.print_with_indent('<write>', level + 1)
			self.currentTokenPosition += 1
			self.expr(level)
		
		else:
			raise Exception()

		self.print_with_indent('</stmt>', level)

	def expr(self, level):
		self.print_with_indent('<expr>', level)
		self.term(level + 1)
		self.term_tail(level + 1)
		self.print_with_indent('</expr>', level)

	def term(self, level: int):

		self.print_with_indent('<term>', level)
		self.factor(level + 1)
		self.fact_tail(level + 1)
		self.print_with_indent('</term>', level)
		return True

	def term_tail(self, level: int):

		self.print_with_indent('<term_tail>', level)

		if self.add_op(level + 1):
			if self.term(level + 1):
				self.term_tail(level + 1)
			else:
				raise Exception
			
		self.print_with_indent('</term_tail>', level)
		

	def factor(self, level: int):
		if self.match('lparen'):
			self.print_with_indent('<lparen>', level)
			self.print_with_indent('(', level + 1)
			self.print_with_indent('</lparen>', level)
			self.currentTokenPosition += 1
			self.expr(level + 1)
			if self.match('rparen'):
				self.print_with_indent('<rparen>', level)
				self.print_with_indent(')', level + 1)
				self.print_with_indent('</rparen>', level)
				self.currentTokenPosition += 1
				return True
			else:
				raise Exception

		elif self.match('id'):
			self.print_with_indent('<id>', level)
			self.print_with_indent(self.tokenValues[self.currentTokenPosition], level + 1)
			self.currentTokenPosition += 1
			self.print_with_indent('</id>', level)
			return True

		elif self.match('number'):
			self.print_with_indent('<number>', level)
			self.print_with_indent(self.tokenValues[self.currentTokenPosition], level + 1)
			self.currentTokenPosition += 1
			self.print_with_indent('</number>', level)
			return True

		return False

	def fact_tail(self, level: int):
		self.print_with_indent('<fact_tail>', level)
		if self.mult_op(level + 1):
			if self.factor(level + 1):
				self.fact_tail(level + 1)
			else:
				raise Exception
		self.print_with_indent('</fact_tail>', level)

	def add_op(self, level: int):
		if self.match('plus'):
			self.print_with_indent('<plus>', level)
			self.print_with_indent('+', level + 1)
			self.currentTokenPosition += 1
			self.print_with_indent('</plus>', level)
			return True
		
		elif self.match('minus'):
			self.print_with_indent('<minus>', level)
			self.print_with_indent('-', level + 1)
			self.currentTokenPosition += 1
			self.print_with_indent('</minus>', level)
			return True

		return False

	def mult_op(self, level):
		if self.match('mult'):
			self.print_with_indent('<times>', level)
			self.print_with_indent('*', level + 1)
			self.currentTokenPosition += 1
			self.print_with_indent('</times>', level)
			return True

		elif self.match('div'):
			self.print_with_indent('<div>', level)
			self.print_with_indent('/', level + 1)
			self.currentTokenPosition += 1
			self.print_with_indent('</div>', level)
			return True
		
		return False

	# Returns true if the next value matches the value provided
	def match(self, value):
		# If we are about to look ahead into out of bounds for the array, return false
		try:
			return self.tokens[self.currentTokenPosition] == value
		except:
			return False


	def print_with_indent(self, value, level: int):
		print(level * '\t' + value)
