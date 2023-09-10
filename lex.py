import enum
from .utils import compareStringsIgnoreCase

class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	KEY = 2
	VALUE = 3
	JSON = 4
	URL = 5
	# Keywords.
	BASIC = 101
	HEADERS = 102
	QUERY = 103
	XWWWURLENCODED = 104
	FORMDATA = 105
	JSONBODY = 106
	DIVIDER = 107
	GET = 108
	POST = 109
	PUT = 110
	DELETE = 111
	PATCH = 112
	# Operators.
	COLON = 201  
	# Protocols
	HTTP = 301
	HTTPS = 302

class Token:
	def __init__(self, tokenText, tokenKind):
		self.text = tokenText
		self.kind = tokenKind

	@staticmethod
	def checkIfKeyword(tokenText):
		for kind in TokenType:
			if compareStringsIgnoreCase(kind.name, tokenText) and kind.value >= 100 and kind.value < 200:
				return kind
		return None

	@staticmethod
	def checkIfProtocol(tokenText):
		for kind in TokenType:
			if compareStringsIgnoreCase(kind.name, tokenText) and kind.value >= 300 and kind.value < 400:
				return kind
		return None

class Lexer:
	def __init__(self, source: str):
		self.source = source + '\n'
		self.curChar = ''
		self.curPos = -1
		self.prevToken = None
		self.nextChar()

	def nextChar(self):
		self.curPos += 1
		if self.curPos >= len(self.source):
			self.curChar = '\0'
		else:
			self.curChar = self.source[self.curPos]

	def peek(self):
		if self.curPos + 1 >= len(self.source):
			return '\0'
		return self.source[self.curPos + 1]

	def prevChar(self):
		if self.curPos - 1 < 0:
			return ''
		i = 1
		prev = self.source[self.curPos - i]
		while prev == ' ' or prev == '\t':
			i += 1
			prev = self.source[self.curPos - i]
		return prev

	def abort(self, message):
		print(f'Lexing error. {message}')

	def skipWhitespace(self):
		while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
			self.nextChar()

	def skipComment(self):
		if self.curChar == '#':
			while self.curChar != '\n':
				self.nextChar()

	def getToken(self):
		self.skipWhitespace()
		self.skipComment()

		print(self.curChar)

		token = None
		if self.curChar == ':':
			token = Token(self.curChar, TokenType.COLON)
		elif self.curChar == '\n':
			token = Token(self.curChar, TokenType.NEWLINE)
		elif self.curChar == '\0':
			token = Token('', TokenType.EOF)
		elif self.curChar == '{' and self.prevChar() != ':':
			bracketsNotClosed = 1
			startPos = self.curPos
			while bracketsNotClosed > 0:
				self.nextChar()
				if self.curChar == '{':
					bracketsNotClosed += 1
				elif self.curChar == '}':
					bracketsNotClosed -= 1
			tokText = self.source[startPos : self.curPos + 1]
			token = Token(tokText, TokenType.JSON)
			print(f'JSON: {tokText}')
		elif self.curChar.isascii() and self.prevChar() != ':':
			startPos = self.curPos
			while self.peek() != ':' and self.peek() != '\n' and self.peek() != '\0' and self.peek() != ' ':
				self.nextChar()
			tokText = self.source[startPos : self.curPos + 1]
			keyword = Token.checkIfKeyword(tokText)
			protocol = Token.checkIfProtocol(tokText)
			if self.prevToken and Token.checkIfProtocol(self.prevToken.text):
				token = Token(tokText, TokenType.URL)
			elif keyword is not None:
				token = Token(tokText, keyword)
			elif protocol is not None:
				self.nextChar()
				if self.curChar != ':':
					raise RuntimeError(f'Lexing error. Expected : after {protocol}')
				self.nextChar()
				if self.curChar != r'/':
					raise RuntimeError(f'Lexing error. Expected / after {protocol} and :')
				self.nextChar()
				if self.curChar != r'/':
					raise RuntimeError(f'Lexing error. Expected / after {protocol} and :/')
				token = Token(tokText, protocol)
			else:
				token = Token(tokText, TokenType.KEY)
		elif self.prevChar() == ':':
			startPos = self.curPos
			while self.curChar != '\n' and self.curChar != '\0':
				self.nextChar()
			tokText = self.source[startPos : self.curPos + 1]
			token = Token(tokText, TokenType.VALUE)
		else:
			raise RuntimeError(f'Unknown token: {self.curChar}')
		self.nextChar()
		self.prevToken = token
		return token














