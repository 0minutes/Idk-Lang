import lexer

def main():
	while (1):
		user = input('>>> ')
		if user == 'exit':
			exit(0)

		tokens = lexer.Lexer(user).tokenize()

		for token in tokens:
			print(token)

if __name__ == '__main__':
	main()