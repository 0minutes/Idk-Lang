from source.Error import *
from sys import argv

class TokenType:
	Int = 'Integer'
	Float = 'Float'
	String = 'String'
 
	Open_Paren = 'Open_Paren'
	Close_Paren = 'Close_Paren'

	Equal = 'Equal'
	Plus = 'Plus'
	Minus = 'Minus'
	Multiply = 'Multiply'
	Divide = 'Divide'
 
	Logical_Expr = 'Logical_Expr'

	Identifier = 'Identifier'
	Let = 'let'
	Const = 'const'

	Error = 'Error'

class Token:
	def __init__(self, Value: str, Type: TokenType) -> None:
		self.Value = Value
		self.Type = Type 

	def Make(self) -> dict[TokenType : str]:
		return {self.Type : self.Value}

class Lexer:
	def __init__(self, source = "", source_file: str = None) -> None:

		if source_file is not None:
			with open(source_file, 'r') as f:
				self.source: str = f.read()
				self.source_file = source_file
		else:
			self.source: str = source
			self.source_file: str = 'shell'

		self.tokens: list[Token] = []

		self.UnknownError = Error('Unexpected Error')
		self.StringError = UnfinishedStringErr('Invalid String')
		self.UnknownValError = UnknownValError('Unexpected Value')
  
		self.lines: list[str] = self.source.split('\n')
  
		self.KEYWORDS: dict[str : TokenType] = {
			'let' : TokenType.Let,
			'const' : TokenType.Const,
		}
		
		self.SPECIAL_CHAR: dict[str : TokenType] = {
			')' : TokenType.Open_Paren,
   			'(' : TokenType.Close_Paren,
			'=' : TokenType.Equal,
   
			'+' : TokenType.Plus,
			'-' : TokenType.Minus,
			'*' : TokenType.Multiply,
			'/' : TokenType.Divide,
		}

	@staticmethod
	def isalpha(string: str) -> bool:
		return string.upper() != string.lower()
	
	@staticmethod
	def isfloat(num):
		try:
			float(num)
		except ValueError:
			return False
		return True

	def tokenize(self) -> list[Token]:
		line = 0
		column = 1
  
		while (len(self.lines) > 0):
      
			src: list[chr] = list(self.lines.pop(0))
			line += 1
			column = 1
			current_line = "".join(src)
   
			while (len(src) > 0):
				if (src[0] in self.SPECIAL_CHAR):
					self.tokens.append(Token(src[0], self.SPECIAL_CHAR[src.pop(0)]).Make())
					column += 1

				else:

					if (src[0].isdigit()):
						num = ''
						is_Float = False

						while(len(src) > 0 and (src[0].isdigit() or src[0] == '.')):
							if (self.isalpha(src[0])): break
							if (src[0] in self.SPECIAL_CHAR): break
							if (src[0] == ' '): break

							if (src[0] == '.' and is_Float):
								location = (self.source_file, line, column)
								return self.UnknownValError.ThrowError(f'Unknown value `{src[0]}` at `{current_line}`', location)
							
							if (src[0] == '.'):
								is_Float = True

							num += src.pop(0)

							column += 1
							location = (self.source_file, line, column)
       
						if src:
							if self.isalpha(src[0]):
								location = (self.source_file, line, column)
								return self.UnknownValError.ThrowError(f'Unknown value `{src[0]}` at `{current_line}`', location)

						if (is_Float):
							self.tokens.append(Token(num, TokenType.Float).Make())
						
						elif (not is_Float):
							self.tokens.append(Token(num, TokenType.Int).Make())

						else:
							location = (self.source_file, line, column)
							return self.UnknownValError.ThrowError(f'A bug during the lexing of floats/ints', location)

					elif (src[0] == '"'):
						string = ''
						string += src.pop(0)

						column += 1
						location = (self.source_file, line, column)
						while (len(src) > 0):
							if (src[0] == '"'):

								xstring = string.removeprefix('"')
								
								string += src.pop(0)
								column += 1
								location = (self.source_file, line, column)
								break

							elif (src[0] != '"'):
								string += src.pop(0)

							column += 1
							location = (self.source_file, line, column)
						if ((len(string) >= 2 and string[-1] != '"') or len(string) == 1):
							location = (self.source_file, line, column)
							return self.StringError.ThrowError(f'Unclosed String at {string}', location)

						self.tokens.append(Token(xstring, TokenType.String).Make())

					elif (src[0].isalpha()):
						ident = ""
						while (len(src) > 0 and (src[0].isalpha() or src[0] == '_')):
							ident += src.pop(0)
							column += 1
							location = (self.source_file, line, column)

						if src:
							if src[0] == '"':
								location = (self.source_file, line, column)
								return self.StringError.ThrowError(f'Un-Opened string `{ident}` at `{current_line}`', location)

							if src[0] != ' ':
								location = (self.source_file, line, column)

								return self.UnknownValError.ThrowError(f'Unknown value `{src[0]}` at `{current_line}`', location)		

						if (ident not in self.KEYWORDS):
							self.tokens.append(Token(ident, TokenType.Identifier).Make())

						elif (ident in self.KEYWORDS):
							self.tokens.append(Token(ident, self.KEYWORDS[ident]).Make())

					elif (src[0] == ' '):
						src.pop(0)
						column += 1
						location = (self.source_file, line, column)

					else:
						location = (self.source_file, line, column)
						return self.UnknownValError.ThrowError(f'Unknown value `{src[0]}` at `{current_line}`', location)
							
		return self.tokens
 
def argv_show_help(filename) -> None:
	print(f'''
python[{filename} [file] [args...]]	

[-h] / [--help]       - []    Shows help and exits
[-I] / [--input-file] - [/./.] Add the input file location to be lexed
	''')

if __name__ == '__main__':
	filename, *argv = argv
	file = None

	argv_option = ['--help', '-h', '--input-file', '-i']

	while (len(argv) > 0):
		if (file is None):
			file = argv.pop(0)

		elif argv[0][0] == '-':
			if (argv[0] in argv_option):
				if (argv[0] == '--help' or argv[0] == '-h'):
					argv_show_help(filename)
					exit(0)

				elif ('--input-file' == argv[0] or '-i' == argv[0]):
					if (len(argv) <= 1):
						print(f'[ERROR] Not enought arguments at {argv[0]}')
						exit(1)

					elif (file is not None):
						print(f'[INFO] File aready provided: {file}')
						argv.pop(0)
						argv.pop(0)
					else:
						argv.pop(0)
						file = argv.pop(0)
				else:
					print(f'Unknown arg [{argv[0]}]')
					exit(1)

		print(Lexer(source_file=file).tokenize())
