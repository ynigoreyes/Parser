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
	
	def program(self, level: int):
		self.print_xml('<program>', level)
		self.stmt_list(level + 1)
		self.print_xml('</program>', level)

	def stmt_list(self, level: int):
		self.print_xml('<stmt_list>', level)
		# If there is still something left to read
		if self.currentTokenPosition < len(self.tokenValues):
			self.stmt(level + 1)
			self.stmt_list(level + 1)
		self.print_xml('</stmt_list>', level)

	def stmt(self, level: int):
		self.print_xml('<stmt>', level)
		# If the next token is an id
		if self.match('id'):
			self.print_xml('<id>', level + 1)
			self.print_xml(self.tokenValues[self.currentTokenPosition], level + 2)
			self.print_xml('</id>', level + 1)
			# Next one should be an assign
			self.currentTokenPosition += 1
			if self.match('assign'):
				self.print_xml('<assign>', level + 1)
				self.print_xml(self.tokenValues[self.currentTokenPosition], level + 2)
				self.print_xml('</assign>', level + 1)
				self.currentTokenPosition += 1
			else:
				raise InvalidTokenExpection()
			self.expr(level + 1)

		elif self.match('read'):
			self.print_xml('<read>', level + 1)
			self.print_xml(self.tokenValues[self.currentTokenPosition], level + 2)
			self.print_xml('</read>', level + 1)
			self.currentTokenPosition += 1
			if self.match('id'):
				self.print_xml('<id>', level + 1)
				self.print_xml(self.tokenValues[self.currentTokenPosition], level + 2)
				self.print_xml('</id>', level + 1)
				self.currentTokenPosition += 1
			else:
				raise InvalidTokenExpection()

		elif self.match('write'):
			self.print_xml('<write>', level + 1)
			self.print_xml('write', level + 2)
			self.print_xml('<write>', level + 1)
			self.currentTokenPosition += 1
			self.expr(level)
		
		else:
			raise InvalidTokenExpection()

		self.print_xml('</stmt>', level)

	def expr(self, level):
		self.print_xml('<expr>', level)
		self.term(level + 1)
		self.term_tail(level + 1)
		self.print_xml('</expr>', level)

	def term(self, level: int):

		self.print_xml('<term>', level)
		self.factor(level + 1)
		self.fact_tail(level + 1)
		self.print_xml('</term>', level)
		return True

	def term_tail(self, level: int):

		self.print_xml('<term_tail>', level)

		if self.add_op(level + 1):
			if self.term(level + 1):
				self.term_tail(level + 1)
			else:
				raise InvalidTokenExpection()
			
		self.print_xml('</term_tail>', level)
		

	def factor(self, level: int):
		if self.match('lparen'):
			self.print_xml('<lparen>', level)
			self.print_xml('(', level + 1)
			self.print_xml('</lparen>', level)
			self.currentTokenPosition += 1
			self.expr(level + 1)
			if self.match('rparen'):
				self.print_xml('<rparen>', level)
				self.print_xml(')', level + 1)
				self.print_xml('</rparen>', level)
				self.currentTokenPosition += 1
				return True
			else:
				raise InvalidTokenExpection

		elif self.match('id'):
			self.print_xml('<id>', level)
			self.print_xml(self.tokenValues[self.currentTokenPosition], level + 1)
			self.currentTokenPosition += 1
			self.print_xml('</id>', level)
			return True

		elif self.match('number'):
			self.print_xml('<number>', level)
			self.print_xml(self.tokenValues[self.currentTokenPosition], level + 1)
			self.currentTokenPosition += 1
			self.print_xml('</number>', level)
			return True

		return False

	def fact_tail(self, level: int):
		self.print_xml('<fact_tail>', level)
		if self.mult_op(level + 1):
			if self.factor(level + 1):
				self.fact_tail(level + 1)
			else:
				raise InvalidTokenExpection
		self.print_xml('</fact_tail>', level)

	def add_op(self, level: int):
		if self.match('plus'):
			self.print_xml('<plus>', level)
			self.print_xml('+', level + 1)
			self.currentTokenPosition += 1
			self.print_xml('</plus>', level)
			return True
		
		elif self.match('minus'):
			self.print_xml('<minus>', level)
			self.print_xml('-', level + 1)
			self.currentTokenPosition += 1
			self.print_xml('</minus>', level)
			return True

		return False

	def mult_op(self, level):
		if self.match('mult'):
			self.print_xml('<times>', level)
			self.print_xml('*', level + 1)
			self.currentTokenPosition += 1
			self.print_xml('</times>', level)
			return True

		elif self.match('div'):
			self.print_xml('<div>', level)
			self.print_xml('/', level + 1)
			self.currentTokenPosition += 1
			self.print_xml('</div>', level)
			return True
		
		return False

	# Returns true if the next value matches the value provided
	def match(self, value):
		# If we are about to look ahead into out of bounds for the array, return false
		try:
			return self.tokens[self.currentTokenPosition] == value
		except:
			return False


	def print_xml(self, value, level: int):
		print(level * '\t' + value)
