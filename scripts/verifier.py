from state import *
from lexer import *
from LTL_tester import *

# Actually takes in and verifies a file/rule combination. 
class Verifier:
	#Setup for the blame option
	def __init__(self):
		self.blame = False
	#Returnes a potential state that might be the cause of the last failed state. 
	def getBlame(self):
		S = self.blameStack.pop()			
		lastState = S
		N = False
		failedOperators = []
		while(S[2] == N and len(self.blameStack)) > 0:
			#A failed negated operator implies a successful subtree and vice-versa
			if(S[0].operator == '~'):
				N = not N
			lastState = S
			failedOperators.append(S)
			S = self.blameStack.pop()
		S = lastState
		return (S,failedOperators)

	#Sets up blame monitoring before evaluation. Then returns the eval() result. 	
	def blameEval(self,token,state):
		self.blame = True
		self.blameStack = []
		s = self.eval(token,state)
		self.blame = False
		return s
	#Evals. 
	#True if the token is true at that state. 
	def eval(self,token,state):
		#Have we already proven this rule for this state?
		if(token.statement in state.getStatements()):
			return True
		#Have we already disproven this rule for this state?
		if("~("+token.statement+")" in state.getStatements()):
			return False
		o = token.operator
		s = None
		if(o == 'proposition'):
			s = self.p(token,state)
		elif(o == '~'):
			s = self.neg(token,state)
		elif(o == 'F'):
			s = self.F(token,state)
		elif(o == 'X'):
			s = self.X(token,state)
		elif(o == 'G'):
			s = self.G(token,state)
		elif(o == 'U'):
			s = self.U(token,state)
		elif(o == 'M'):
			s = self.M(token,state)
		elif(o == 'W'):
			s = self.W(token,state)
		elif(o == 'R'):
			s = self.R(token,state)
		elif(o == '&'):
			s = self.both(token,state)
		elif(o == "|"):
			s = self.either(token,state)
		elif(o==">"):
			s = self.implies(token,state)
		elif(o=="="):
			s = self.equals(token,state)
			
		if(s == None):
			raise ValueError("Unknown token operator " + token.operator)
			
		#We've either proven or disproven the statement now, add that knowledge to the state. 
		if(s):
			state.addStatement(token.statement)
		else:
			state.addStatement("~("+token.statement+")")
		if(self.blame):
			self.blameStack.append((token,state,s))
			
		return s
		
	#Proposition, just check if state has proposition
	def p(self,token,state):
		return token.statement in state.getVariables()
		
	#NOT
	def neg(self,token,state):
		return not self.eval(token.phi,state)
		
	#And 
	def both(self,token,state):
		return self.eval(token.phi,state) and self.eval(token.psi,state)
		
	#OR
	def either(self,token,state):
		return self.eval(token.phi,state) or self.eval(token.psi,state)
		
	#Some future state. Walk along the graph, testing the subtree for each encountered state.
	#Fail if we get to the end of the path or in a circle without proving the statement. 
	def F(self,token,state):
		if(self.eval(token.phi,state)):
			return True
		visited = []

		state = state.getNext()
		while(state != None and state.id not in visited):
			if(self.eval(token.phi,state)):
				return True
			visited.append(state.id)
			state = state.getNext()
		return False
		
	#Eval rule on next state
	def X(self,token,state):
		nextState = state.getNext()
		if(nextState == None):
			return False
		return self.eval(token.phi,nextState)
		
	#Eval rule for every state remaining on the path. Fail if we can disprove it before going in a circle or dead end. 
	def G(self,token,state):
		if(not self.eval(token.phi,state)):
			return False 
		
		visited = []
		state = state.getNext()
		while(state != None and state.id not in visited):
			if(not self.eval(token.phi,state)):
				return False
			visited.append(state.id)
			state = state.getNext()
			
		return True
		
	#.. I left a print("AAAAAAAAAAAAAA") in the project among other prints. This is why we have code review in the real world. 
	#a Until b, test if a holds on every single state up to a state where b holds.
	# Strong, b must happen
	def U(self,token,state):
		#print("AAAAAAAAAAAAAAAA")
		phi = token.phi 
		psi = token.psi
		
		if(self.eval(psi,state)):
			#print(str(state.id) + " INSTA FREE")
			return True
		else:
			if(not self.eval(phi,state)):
				#print(state.id + " (Instant deliver) Broke U")
				return False 
		
		visited = []
		state = state.next
		while(state != None and state.id not in visited):
			if(self.eval(psi,state)):
				#print(str(state.id) + " FREE")
				return True
			else:
				if(not self.eval(phi,state)):
					#print(state.id + " (Late deliver) Broke U")
					return False 
			visited.append(state.id)
			state = state.getNext()
			
		print(state.id + " (Never) Broke U")
		return False #Psi must hold in the end, we got into a dead end and never saw it.
		
	#Weak release.
	#Same as release, but returns True if we get to the end of path / circle before disproving the rule
	def M(self,token,state):
		phi = token.phi 
		psi = token.psi
		if(self.eval(psi,state)):
			return self.eval(phi,state) #Both must hold at the same time
		else:
			if(not self.eval(phi,state)):
				return False 
		
		visited = []
		state = state.next
		while(state != None and state.id not in visited):
			if(self.eval(psi,state)):
				return self.eval(phi,state) #Both must hold at the same time
			else:
				if(not self.eval(phi,state)):
					return False 
			visited.append(state.id)
			state = state.getNext()
			
		return True #Phi is still holding
			
	#Weak until
	#Same as until, sans print statements, but will return true if the rule holds until a circle is reached / dead node. 
	def W(self,token,state):
		phi = token.phi 
		psi = token.psi
		
		if(self.eval(psi,state)):
			return True
		else:
			if(not self.eval(phi,state)):
				return False 
		
		visited = []
		state = state.next
		while(state != None and state.id not in visited):
			if(self.eval(psi,state)):
				return True
			else:
				if(not self.eval(phi,state)):
					return False 
			visited.append(state.id)
			state = state.getNext()
			
		return True #Psi does not have to occur
		
	#Release.
	# a R b implies a MUST hold up to AND INCLUDING the state b holds. 
	# IF b never happens, fail. 
	def R(self,token,state):
		phi = token.phi 
		psi = token.psi
		if(self.eval(psi,state)):
			return self.eval(phi,state) #Both must hold at the same time
		else:
			if(not self.eval(phi,state)):
				return False 
		
		visited = []
		state = state.next
		while(state != None and state.id not in visited):
			if(self.eval(psi,state)):
				return self.eval(phi,state) #Both must hold at the same time
			else:
				if(not self.eval(phi,state)):
					return False 
			visited.append(state.id)
			state = state.getNext()
			
		return False 
		
	# if a, then b. if a and not b, fail. 
	def implies(self,token,state):
		return (not self.eval(token.phi,state)) or (self.eval(token.psi,state))
		
	# a and b must either both be true or both be false for this state.
	def equals(self,token,state):
		return self.eval(token.phi,state) == self.eval(token.psi,state)
# p ~ F X G U M W R & |
