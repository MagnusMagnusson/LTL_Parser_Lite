# Accepted language:
# + = F(+) : X(+) : G(+) : ~(+) : (+)R(+) : (+)M(+) : (+)U(+) : (+)W(+) : (+)&(+) : (+)|(+) : p
class Token:
	def __init__(self,operator,phi,psi,statement):
		self.operator = operator
		self.phi = phi 
		self.psi = psi
		self.statement = statement
	def printTree(self,level):
		space = str(level)+". " + "    " * level
		if(self.operator == 'proposition'):
			print(space + self.statement)
			return
		
		print(space + self.operator)
		if(self.phi != None):
			self.phi.printTree(level + 1)
		if(self.psi != None):
			self.psi.printTree(level + 1)
	
class lexer:
	def statement(self, statement):
		print(statement)
		if(len(statement) == 0):
			raise ValueError("Empty statement detected!")
		operators = ["F","R","X","G","U","W","M","~","&","|","(",")"]
		proposition = True
		for o in operators:
			if(o in statement):
				proposition = False
				break
		
		if(proposition):
			if(not statement.islower()):
				raise ValueError("Propositions must be lower case: " + statement)
			token = Token("proposition",None,None,statement)
			return token
		unary = ["F","X","G","~"]
		if(statement[0] in unary):
			operator = statement[0]
			phi = self.statement(statement[2:-1])
			token = Token(operator,phi,None,statement)
			return token
		if(statement[0] != '('):
			raise ValueError("Malfunctioned statement[1], all statements must begin with '(': " + statement)
		c = 1
		endPoint = 0
		phiStatement = ""
		for i in range(1,len(statement)):
			if(statement[i] == '('):
				c += 1
			if(statement[i] == ')'):
				c -= 1
			if(c == 0):
				phiStatement = statement[1:i]
				endPoint = i 
				break
			
		endPoint += 1
		
		phi = self.statement(phiStatement)
		
		binary = ["R","M","W","U","&","|"]
		if(not statement[endPoint] in binary):
			raise ValueError("Missing binary operator: " + statement)
		
		operator = statement[endPoint]
		endPoint += 1
		
		if(statement[endPoint] != '('):
			raise ValueError("Malfunctioned statement[2], all nested statements must begin with '(': " + statement)
			
		c = 1
		psiStatement = ""
		for i in range(endPoint + 1,len(statement)):
		  if(statement[i] == '('):
				c += 1
		  if(statement[i] == ')'):
			c -= 1
		  if(c == 0):
			psiStatement = statement[endPoint+1:i]
			endPoint = i+1
			break
		psi = self.statement(psiStatement)
		if(endPoint != len(statement)):
			raise ValueError("Statement did not end after second binary predicate: " + statement)
		
		token = Token(operator,phi,psi,statement)
		return token 
			
class state:
	
	def __init__(self):
		self.next = None
		self.variables = []
		self.statements = []
		self.visited = 0
		
	def getVariables(self):
		return self.variables
		
	def setVariables(self,variables):
		self.variables = variables
		
	def getStatements(self):
		return self.statements
		
	def setStatements(self,statements):
		self.statements = statements

	def addStatement(self,statement):
		if(statement in self.statements):
			return
		self.statements.add(statement)
		
	def next(self):
		return self.next
	
	def setNext(self,node):
		self.next = node 
		
	def printLoop(self,ID):
		if(self.visited == 1):
			print("LOOP AT " + str(self.ID))
			return
		self.visited = 1
		self.ID = ID
		print(str(ID) + " : " + str(self.variables))
		if(self.next == None):
			print("TERMINATED")
		else:
			self.next.printLoop(ID + 1)
		self.visited = 0
		
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
