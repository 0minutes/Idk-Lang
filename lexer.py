from typing import Union

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
	def __init__(self, source) -> None:
		self.tokens: list[Token] = []
		self.source: str = source

		self.line: int = 0
		self.cursor: int = 1
		self.lines: list[str] = source.split('\n')
		self.cur_line = self.lines[self.line]

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

	def isskippable(self, string: str) -> bool:

		if (string == '\n'):
			self.line += 1
			self.cursor = 0
			return True

		return False

	def ThrowError(self, message: str) -> list[str]:
		return [f'[ERROR] line: {self.line+1}, Col: {self.cursor}: {message}']

	def tokenize(self) -> list[Token]:
		src: list[chr] = list(self.source)
		while (len(src) > 0):

			if (len(src) > 1):
				next_char = src[1]
			else:
				next_char = None


			if (src[0] == '('):
				self.cursor += 1
				self.tokens.append(Token(src.pop(0), TokenType.Open_Paren).Make())
				next_char = src[1] if len(src) > 1 else None

			elif (src[0] == ')'):
				self.cursor += 1
				self.tokens.append(Token(src.pop(0), TokenType.Close_Paren).Make())
				next_char = src[1] if len(src) > 1 else None

			elif (src[0] == '='):
				self.cursor += 1
				self.tokens.append(Token(src.pop(0), TokenType.Equal).Make())
				next_char = src[1] if len(src) > 1 else None

			elif (src[0] in ('+', '-', '*', '/')): 
				self.cursor += 1
				self.tokens.append(Token(src.pop(0), TokenType.Operation).Make()) 
				next_char = src[1] if len(src) > 1 else None

			else:
				if (self.isskippable(src[0])):
					src.pop(0)
					next_char = src[1] if len(src) > 1 else None
					continue

				if (src[0].isdigit()):
					
					num = ''
					is_Float = False

					while(len(src) > 0 and (src[0].isdigit() or src[0] == '.')):

						if (src[0] == ' '): break

						if (src[0] == '.' and is_Float):
							return ThrowError(f'Unknown value {src[0]} at {self.cur_line}')

						if (src[0] == '.'):
							is_Float = True

						num += src.pop(0)

						self.cursor += 1

					next_char = src[1] if len(src) > 1 else None
					
					if src:
						if src[0] != ' ':
							return self.ThrowError(f'Unknown value `{src[0]}` at `{self.cur_line}`')
					
					if (is_Float):
						self.tokens.append(Token(num, TokenType.Float).Make())
					
					elif (not is_Float):
						self.tokens.append(Token(num, TokenType.Int).Make())

				elif (src[0] == '"'):
					string = ''
					string += src.pop(0)
					next_char = src[1] if len(src) > 1 else None

					self.cursor += 1
					while (len(src) > 0):
						if (src[0] == '"'):

							xstring = string.removeprefix('"')
							
							string += src.pop(0)
							self.cursor += 1
							break

						elif (src[0] != '"'):
							string += src.pop(0)

						self.cursor += 1

					if((len(string) >= 2 and string[-1] != '"') or len(string) == 1):
						return self.ThrowError(f"Un-Closed String at `{self.cur_line}`")

					self.tokens.append(Token(xstring, TokenType.String).Make())

				elif (src[0].isalpha()):
					ident = ""
					while (len(src) > 0 and (src[0].isalpha() or src[0] == '_')):
						ident += src.pop(0)
						self.cursor += 1

					if src:
						if src[0] == '"':
							return self.ThrowError(f'Un-Opened String `{ident}` at `{self.cur_line}`')

						if src[0] != ' ':
							return self.ThrowError(f'Unknown value `{src[0]} at `{self.cur_line}`')

					if (ident not in self.KEYWORDS):
						self.tokens.append(Token(ident, TokenType.Identifier).Make())

					elif (ident in self.KEYWORDS):
						self.tokens.append(Token(ident, self.KEYWORDS[ident]).Make())

				elif (src[0] == ' '):
					src.pop(0)
					self.cursor += 1

				else:
					return self.ThrowError(f'Unknown value `{src[0]}` at `{self.cur_line}`')
					exit(1)

		return self.tokens
