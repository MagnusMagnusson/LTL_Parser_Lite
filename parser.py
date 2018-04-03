import lexer	
import state
		
class parser:
	def __init__(self):
		self.file = 0
	def setFile(self, file):
		self.file = file
	def parsePath(self):
		beginnerNode = None
		nowNode = None
		loopNode = None
		fileobj = open(self.file, "r")
		length = 0
		loop = 0
		first = True
		
		for line in fileobj:
			if(first):
				s = line.split()
				length = int(s[0])
				loop = int(s[1])
				first = False
			else:
				newNode = state()
				if(beginnerNode == None):
					beginnerNode = newNode
				variables = line.split()
				newNode.setVariables(variables)
				if(nowNode != None):
					nowNode.setNext(newNode)
				nowNode = newNode
				if(length == loop):
					loopNode = newNode
				length -= 1
		if(loopNode != None and loopNode != nowNode):
			nowNode.setNext(loopNode)
		return beginnerNode
		



lexer = lexer()
root = lexer.statement("(F(G(X(p))))&(F((~(q))R(~(X(z)))))")
root.printTree(0)
