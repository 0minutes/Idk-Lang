from source.Error import *

class TokenType:
	Int = 'Integer'
	Float = 'Float'

	String = 'String'
	Identifier = 'Identifier'
	Equal = 'Equal'
	Open_Paren = 'Open_Paren'
	Close_Paren = 'Close_Paren'

	Operation = 'Operation'
	Logical_Expr = 'Logical_Expr'

	Let = 'let'
	Const = 'const'

class Token:
	def __init__(self, Value: str, Type: TokenType) -> None:
		self.Value = Value
		self.Type = Type 

	def Make(self) -> dict[TokenType : str]:
		return {self.Type : self.Value}

class Lexer:
	def __init__(self, source = "",source_file: str = None) -> None:

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
			current_line = "".join(src)
   
			while (len(src) > 0):
				if (src[0] == '('):
					column += 1
					location = (self.source_file, line, column)
     
					self.tokens.append(Token(src.pop(0), TokenType.Open_Paren).Make())

				elif (src[0] == ')'):
					column += 1
					self.tokens.append(Token(src.pop(0), TokenType.Close_Paren).Make())

				elif (src[0] == '='):
					column += 1
					location = (self.source_file, line, column)
					self.tokens.append(Token(src.pop(0), TokenType.Equal).Make())

				elif (src[0] in ('+', '-', '*', '/')): 
					column += 1
					self.tokens.append(Token(src.pop(0), TokenType.Operation).Make()) 

				else:

					if (src[0].isdigit()):
						num = ''
						is_Float = False

						while(len(src) > 0 and (src[0].isdigit() or src[0] == '.')):

							if (src[0] == ' '): break

							if (src[0] == '.' and is_Float):
								location = (self.source_file, line, column)
								return self.UnknownValError.ThrowError(f'Unknown value `{src[0]}` at `{self.lines}`', location)

							if (src[0] == '.'):
								is_Float = True

							num += src.pop(0)

							column += 1
							location = (self.source_file, line, column)
						if src:
							if src[0] != ' ':
								location = (self.source_file, line, column)
								return self.UnknownValError.ThrowError(f'Unknown value `{src[0]}` at `{current_line}`', location)
						
						if (is_Float):
							self.tokens.append(Token(num, TokenType.Float).Make())
						
						elif (not is_Float):
							self.tokens.append(Token(num, TokenType.Int).Make())

						else:
							location = (self.source_file, line, column)
							return self.UnknownError.ThrowError('A bug during the lexing of the integers/floats', location)

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
							return self.StringError.ThrowError(f"Un-Closed String at `{current_line}`", location)

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
								return self.StringError.ThrowError(f'Un-Opened String `{ident}` at `{current_line}`', location)

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
 
if __name__ == '__main__':
    for token in Lexer(source_file='source/source.txt').tokenize():
        print(token)