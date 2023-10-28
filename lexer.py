class TokenType:
	Number = 'Number'
	Identifier = 'Identifier'
	Equal = 'Equal'
	Open_Paren = 'Open_Paren'
	Close_Paren = 'Close_Paren'

	Operation = 'Operation'
	Logical_Expr = 'Logical_Expr'

	let = 'let'
	const = 'const'

KEYWORDS: dict[str : TokenType] = {
	'let' : TokenType.let,
}

def isalpha(string: str) -> bool:
	return string.upper() != string.lower()

def isskippable(string: str) -> bool:
	if (string == ' ' or string == '\n' or string == '\t'):
		return True
	return False

def tokenize(Value: str, Type: TokenType) -> dict[str : TokenType]:
	return {'value': Value, 'type': Type}

def lexer(source: str) -> list[dict[str : TokenType]]:
	tokens: list[dict[str : TokenType]] = []
	src: list[str] = list(source)
	cursor: int = 0

	while (len(src) > 0):
		if (src[0] == '('): tokens.append(tokenize(src.pop(0), TokenType.Open_Paren))
		elif (src[0] == ')'): tokens.append(tokenize(src.pop(0), TokenType.Close_Paren))
		
		elif (src[0] == '='): tokens.append(tokenize(src.pop(0), TokenType.Equal))
		elif (src[0] in ('+', '-', '*', '/')): tokens.append(tokenize(src.pop(0), TokenType.Operation)) 

		else:
			if (isskippable(src[0])):
				src.pop(0)
				continue

			elif (src[0].isdigit()):
				num = ""
				while (len(src) > 0 and src[0].isdigit()):
					num += src.pop(0)

				tokens.append(tokenize(num, TokenType.Number))

			elif (src[0].isalpha()):
				ident = ""
				while (len(src) > 0 and src[0].isalpha()):
					ident += src.pop(0)

				if (ident not in KEYWORDS):
					tokens.append(tokenize(ident, TokenType.Identifier))
				else:
					tokens.append(tokenize(ident, KEYWORDS[ident]))
			
			else:
				print(f'Unrecognized value in `{src[0]}`')
				exit(1)

	return tokens

print(lexer('let foo = 4 - ( 3 * 6 )'))