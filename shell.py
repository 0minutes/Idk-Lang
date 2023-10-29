from source.lexer import Lexer

def main():
	while (1):
		shell = input('>>> ')
		if shell == 'exit':
			exit(0)

		tokens = Lexer(source=shell)

		for token in tokens.tokenize():
			print(token)

if __name__ == '__main__':
	main()