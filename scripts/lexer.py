# Accepted language:
# + = F(+) : X(+) : G(+) : ~(+) : (+)R(+) : (+)M(+) : (+)U(+) : (+)W(+) : (+)&(+) : (+)|(+) : > : p
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
	def __init__(self):
		self.variables = {}
	def addVariable(self,variable,definition):
		self.variables[variable] = definition
	def getVariable(self,variable):
		return self.variables[variable]
	def getAllVariables(self):
		return self.variables.keys()
		
	def statement(self, statement):
		statement = statement.strip()
		
		operators = ["F","R","X","G","U","W","M","~","&","|","(",")",">","=","{","}"]
		
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
		
		if(len(statement) == 0):
			raise ValueError("Empty statement detected!")
		if(statement[0] == '('):
			c = 0
			for i in range(len(statement)):
				character = statement[i]
				if character == '(':
					c += 1
				if character == ')':
					c -= 1
				if c == 0:
					if i == len(statement) - 1:
						newStatement = statement[1:-1]
						return self.statement(newStatement)
					else:
						break
		if(statement[0] == '{' and statement[-1] == '}'):			
			c = 0
			for i in range(len(statement)):
				character = statement[i]
				if character == '{':
					c += 1
				if character == '}':
					c -= 1
				if c == 0:
					if i == len(statement) - 1:
						return self.getVariable(statement)
					else:
						break
			
					
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
		
		binary = ["R","M","W","U","&","|",">","="]
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
		
		token = Token(operator,phi,psi,statement)
		return token 
		
	def parse(self,statement):
		precedence = [["R","U","W","M"],[">","="],["&","|"],["G","F","X"],["~"]]
		i = 0
		for group in precedence:
			i = 0
			while i < len(statement):
				char = statement[i]
				if(char in group):
					binary = ["R","U","W","M",">","=","&","|"]
					s1 = statement[:i]
					s2 = statement[i+1:]
					if(char in binary):
						return "("+self.parse(s1)+")"+char+"("+self.parse(s2)+")"
					else:
						return  self.parse(s1)+char+"("+self.parse(s2)+")"
				i+=1
		return statement
			
	def enclosed(self,string):
	  if(len(string) == 0):
		return True
		
	  if(string[0] != "("):
		return False
	  c = 0
	  for j in range(len(string)):
		char2 = string[j]
		if(char2 == '('):
		  c += 1 
		if(char2 == ')'):
		  c -= 1
		if(c == 0):
		  return j == len(string) - 1
	  return True
	  
	def extraParen(self,string):
	  returnString = ""
	  i = 0
	  while i < len(string):
		char = string[i]
		if(char == '('):
		  s = ""
		  c = 0
		  for j in range(i,len(string)):
			char2 = string[j]
			s += char2
			if(char2 == '('):
			  c += 1 
			if(char2 == ')'):
			  c -= 1
			if(c == 0):
			  break
		  i = j
		  inner = self.extraParen(s[1:-1])
		  if(self.enclosed(inner)):
			returnString += inner
		  else:
			returnString += "("+inner+")"
		else:
		  returnString += char
		
		i += 1
	  return returnString