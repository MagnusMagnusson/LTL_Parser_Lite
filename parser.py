from lexer import *
from state import *
from verifier import *  
import sys 

class parser:
	def parsePath(self,file):
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
				newNode = state()
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
		
		return beginnerNode
		
	def parseEquations(self,file):
		equations = []
		fileobj = open(file, "r")
		lex = lexer()
		for line in fileobj:
			rule = line.split(':')
			try:
				rootToken = lex.statement(rule[1])
				equations.append((rule[0],rootToken))
			except ValueError as E:
				print("Error lexing rule '" + str(rule[0]) + "'")
				print("Error returned: " + str(E))
				
		return equations


sys.stdout.flush()
p = parser()
sys.stdout.flush()
v = Verifier()
sys.stdout.flush()
rules = p.parseEquations("equations.txt")
sys.stdout.flush()
path = p.parsePath("paths/testPath.txt")
sys.stdout.flush()
for rule in rules:
	print("Testing rule: " + rule[0])
	sys.stdout.flush()
	if(v.eval(rule[1],path)):
		print("Rule valid")
		sys.stdout.flush()
	else:
		print("Rule failed")
		sys.stdout.flush()
