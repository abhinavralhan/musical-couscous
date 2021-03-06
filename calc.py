INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, POW, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', '(', ')', 'POW', 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]


    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)


    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        count = 0

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '(':
            	count = count + 1
            	self.advance()
            	return Token(LPAREN, '(')

            if self.current_char == ')':
                count = count - 1
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            # if self.current_char == '**':
            #     self.advance()
            #     return Token(POW, '**')
            self.error()
        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
    	result = self.factor()
    	while self.current_token.type in (MULTIPLY,DIVIDE):
    		token = self.current_token
    		if token.type == MULTIPLY:
    			self.eat(MULTIPLY)
    			result = result * self.factor()
    		elif token.type == DIVIDE:
    			self.eat(DIVIDE)
    			result = result / self.factor()
    	return result
	

    def expr(self):
	    result = self.term()
	    while self.current_token.type in (PLUS, MINUS):
	    	token = self.current_token
	    	if token.type == PLUS:
	    		self.eat(PLUS)
	    		result = result + self.term()
	    	elif token.type == MINUS:
	    		self.eat(MINUS)
	    		result = result - self.term()
	    return result


def main():
	print('\nSimple Calculator\n(type exit to leave)\n')
	while True:
		try:
			text = input('calculate > ')
		except EOFError:
			break
		if text == "exit":
			print('bye bye')
			return
		if not text:
			continue
		lexer = Lexer(text)
		interpreter = Interpreter(lexer)
		result = interpreter.expr()
		print(result)

if __name__ == '__main__':
	main()
