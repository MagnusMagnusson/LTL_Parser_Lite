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