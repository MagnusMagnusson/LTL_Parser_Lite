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
	def statement(self, statement):
		statement = statement.strip()
		if(len(statement) == 0):
			raise ValueError("Empty statement detected!")
		operators = ["F","R","X","G","U","W","M","~","&","|","(",")",">"]
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
	