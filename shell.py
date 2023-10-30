from source.lexer import Lexer

def main():
	while (1):
		shell = input('>>> ')
		if shell == 'exit':
			exit(0)

		tokens = Lexer(source=shell)

		print(tokens.tokenize())

if __name__ == '__main__':
	main()