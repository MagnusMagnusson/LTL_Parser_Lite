import lexer
import state

class Parser:
	def __init__(self):
		self.yolo = "why"
		print self.yolo
	def parsePath(self,files):
		paths = []
		for file in files:
			beginnerNode = None
			nowNode = None
			loopNode = None
			fileobj = open(file, "r")
			length = 0
			loop = 0
			first = True
			nodeID = 0
			
			for line in fileobj:
				if(first):
					s = line.split()
					length = int(s[0])
					loop = int(s[1])
					first = False
				else:
					newNode = state.state()
					newNode.id = nodeID
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
					nodeID += 1
			if(loopNode != None and loopNode != nowNode):
				nowNode.setNext(loopNode)
			fileobj.close()
			paths.append(beginnerNode)
			
		return paths
		
	
	def parseEquations(self,files):
		equations = []
		for file in files:
			fileobj = open(file, "r")
			lex = lexer.lexer()
			for line in fileobj:
				rule = line.split(':')
				try:
					rootToken = lex.statement(rule[1])
					equations.append((rule[0],rootToken))
				except ValueError as E:
					print("Error lexing rule '" + str(rule[0]) + "'")
					print("Error returned: " + str(E))
			fileobj.close()
				
		return equations

