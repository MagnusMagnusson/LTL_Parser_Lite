
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
		
