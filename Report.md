# Parser Pseudo-code
* Introduction
	* We built a parser that prints out the XML for some program. The parser uses an upgraded version of the Scanner we created from project 1 (that is why our code looks so similar to project 1 submission). We added the ability to see the value of the tokens as they are read from the Scanner. This makes it easier to print out the values of the tokens when running the Parser.
	* We decided to use a tuple of arrays, one array containing the type of token and the other being the values of the tokens.
	* The indices are used to relate the two arrays. Example: array1[x] is the type of token given array2[x] where x is some integer less than the length of the arrays
* Steps
	* Find the tokens using project 1 scanner and see if there are any errors with the tokens found. That way we can fail fast.
	* Add functionality to the scanner to return a tuple containing the type of expression and the value of the expression instead of just the type. This is so that we can print it out
	* Pass the level of indentation to each function

// Function we use to start off the entire recursive decent
// Within each nested function call, we must pass the indentation level to the next level

main():
	// This is where we start off the entire parsing
	program()

// for the sake of readability, assume that every function bellow accepts a “level” of type int describing the current level of indentation

program():
	print <Program>
	stmt_list()
	print </Program>
	end program

stmt_list()
	print <stmt_list>
	if there is nothing left to read:
		return
	else:
		stmt()
		stmt_list()
	print </stmt_list>

stmt():
	print <stmt>
	if next token is an id:
		print <id>
		print the value of the id
		print </id>
		print <assign>
		print the value for assign
		print </assign>
	else if next token is read:
		print <read>
		print read
		print </read>
	else if next token is write
		print <write>
		expr()
		print </write>
	print </stmt>
		
expr()
	print <expr>
	term()
	term_tail()
	print </expr>

term()
	print <term>
	factor()
	fact_tail()
	print </term>

term_tail()
	print <term_tail>
	if add_op():
		if term():
			term_tail()
	print </term_tail>

factor():
	print <factor>

	if next character is id:
		print <id>
		print value of id
		print </id>
	if next character is number:
		print <number>
		print value for number
		print </number>
	else:
		print <lparen>
		print “(“
		print </lparen>
		expr()
		print <rparen>
		print “)“
		print </rparen>

	print </factor>

fact_tail()
	print <fact_tail>
	if mult_op():
		if factor():
			fact_tail()
	print </fact_tail>

add_op()
	print <add_op>
	print value of add_opp (should be plus or minus)
	print </add_op>

mult_op()
	print <mult_op>
	print value of mult_opp (should be times or div)
	print </mult_op>

Test Cases:
1. y = 7
2. x := 7
3. read A
4. One with comments
5. write 1 + 2

We wanted to handle all of the simple valid examples as well as a simple example where one fails (number 1, bad assignment)

People working on this Project
* Ynigo Reyes
	* report
	* factor
	* fact_tail
	* add_op
* William Tomah
	* report
	* stmt
	* stmt_list
	* expr

