from state import *
from lexer import *
from LTL_tester import *

# p ~ F X G U M W R & |
class Verifier:

	def __init__(self):
		self.blame = False
	def getBlame(self):
		S = self.blameStack.pop()			
		lastState = S
		N = False
		failedOperators = []
		while(S[2] == N):
			if(S[0].operator == '~'):
				N = not N
			lastState = S
			failedOperators.append(S)
			S = self.blameStack.pop()
		S = lastState
		return (S,failedOperators)

		
	def blameEval(self,token,state):
		self.blame = True
		self.blameStack = []
		s = self.eval(token,state)
		self.blame = False
		return s
	def eval(self,token,state):
		if(token.statement in state.getStatements()):
			return True
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
			
		if(s):
			state.addStatement(token.statement)
		else:
			state.addStatement("~("+token.statement+")")
		if(self.blame):
			self.blameStack.append((token,state,s))
			
		return s
		
	def p(self,token,state):
		return token.statement in state.getVariables()
		
	def neg(self,token,state):
		return not self.eval(token.phi,state)
		
	def both(self,token,state):
		return self.eval(token.phi,state) and self.eval(token.psi,state)
		
	def either(self,token,state):
		return self.eval(token.phi,state) or self.eval(token.psi,state)
		
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
		
	def X(self,token,state):
		nextState = state.getNext()
		if(nextState == None):
			return False
		return self.eval(token.phi,nextState)
		
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
		
	def U(self,token,state):
		print("AAAAAAAAAAAAAAAA")
		phi = token.phi 
		psi = token.psi
		
		if(self.eval(psi,state)):
			print(str(state.id) + " INSTA FREE")
			return True
		else:
			if(not self.eval(phi,state)):
				print(state.id + " (Instant deliver) Broke U")
				return False 
		
		visited = []
		state = state.next
		while(state != None and state.id not in visited):
			if(self.eval(psi,state)):
				print(str(state.id) + " FREE")
				return True
			else:
				if(not self.eval(phi,state)):
					print(state.id + " (Late deliver) Broke U")
					return False 
			visited.append(state.id)
			state = state.getNext()
			
		print(state.id + " (Never) Broke U")
		return False #Psi must hold in the end, we got into a dead end and never saw it.
		
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
		
	def implies(self,token,state):
		return (not self.eval(token.phi,state)) or (self.eval(token.psi,state))
		
	def equals(self,token,state):
		return self.eval(token.phi,state) == self.eval(token.psi,state)
# p ~ F X G U M W R & |
