import sys
import os
from os import listdir
from os.path import isfile, join
sys.path.append('scripts/')
import pathParser
from verifier import * 


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	
def printHelp():	
	print(bcolors.HEADER +"LTL model checker help"+bcolors.ENDC)
	print("\n")
	print("Usage: "+ sys.argv[0] + " [OPTIONS] [PATHS] [RULES]")
	print("[OPTIONS] : optional program parameters for specific option behaviors (see below)")
	print("[PATHS] : File or directory containing path files. Every file found in the specified directory will be tested. Non-recursive")
	print("[RULES] : File or directory containing LTL rules to test against. Every file found in the specified directory will be tested against. Non-recursive")
	print("\n")
	print("OPTIONS:")
	print("'s' : 'Silent'. Will cause the program to output as little as it can, only printing negative test results")
	print("'b' : 'Blame'. Any test that fails will output the state where the test is suspected to have failed in, along with its propositions")
	print("'t' : 'Trace'. Any test that fails will print out the entire evaluation stack trace leading to the failed rule. Requires 'Blame'") 
	print("'g' : 'Grayscale'. Disables colors in output. Preferable for shells that do not support ANSI escape codes.") 

	
if __name__ == "__main__":	

	argument_count = len(sys.argv)
	if(argument_count == 2 and sys.argv[1] == "--help"):
		printHelp()
		sys.exit(0)
	if(argument_count != 3 and argument_count != 4):
		print("Usage: "+ sys.argv[0] + " [OPTIONS] [PATHS] [RULES]")
		print("Try '"+ sys.argv[0] + " --help' for help")
		sys.exit(0)
		
	print(bcolors.HEADER +"===================================================")
	print("======= Welcome to the LTL model checker. =========")
	print("===================================================" +bcolors.ENDC)
	

		
	i = 0
	silent = False
	collect = False
	blame = False
	trace = False
	
	if(argument_count == 4):
		i = 1
		options = sys.argv[1]
		silent = 's' in options
		collect = 'c' in options
		blame = 'b' in options
		trace = 't' in options
		if('g' in options):
			bcolors.OKGREEN = ""
			bcolors.OKBLUE = ""
			bcolors.FAIL = ""
			bcolors.ENDC = ""
			bcolors.WARNING = ""
		
	paths = sys.argv[1+i]
	rules = sys.argv[2+i]
	
	pathDir = None 
	ruleDir = None
	if(os.path.isfile(paths)):
		pathDir = False
	elif(os.path.isdir(paths)):
		pathDir = True
	
	
	if(os.path.isfile(rules)):
		ruleDir = False
	elif(os.path.isdir(rules)):
		ruleDir = True
		
	if(pathDir == None):
		print("Error: Unable to find file or directory " + paths)
		sys.exit(0)
	if(ruleDir == None):
		print("Error: Unable to find file or directory " + rules)
		
	if(pathDir == True):
		allPaths = [join(paths, f) for f in listdir(paths) if isfile(join(paths, f))]
	else:
		allPaths = [paths]
	if(ruleDir == True):
		allRules = [join(rules, f) for f in listdir(rules) if isfile(join(rules, f))]
	else:
		allRules = [rules]
		
	print("Path files being tested:\n" + str(allPaths)+"\n")
	print("Rule files being tested:\n" + str(allRules)+"\n")
	
	if True:
		p = pathParser.Parser()
		v = Verifier()
		print("-----Starting tests!-----")
		for path in allPaths:
			if(not silent):
				print("Testing path " + path)
			node = p.parsePath([path])[0]
			
			for r in allRules:
				if(not silent):
					print("    Testing ruleset " + r)
				expressions = p.parseEquations([r])
				for expression in expressions:
					if(not silent):
						sys.stdout.write("        Testing rule '" + expression[0] + "\r")
					if(v.blameEval(expression[1],node)):
						if(not silent):
							sys.stdout.write(bcolors.OKGREEN + "        PASSED - Testing rule" + bcolors.ENDC+" '" + expression[0] + "'\n\r" )
							sys.stdout.flush()
					else:
						s = ""
						if(silent):
							s = "["+ path + "," + r + "]."
						sys.stdout.write(bcolors.FAIL+"        FAILED - Testing rule "+bcolors.ENDC+s+"'" + expression[0] + "'"  + "\n\r")
						if(blame):
							blameState = v.getBlame()
							print(bcolors.WARNING+"            Potential counterexample at or near state " + str(blameState[0][1].id))
							print("            State propositions: " + str(blameState[0][1].getVariables()) + bcolors.ENDC)
							if(trace):
								for S in blameState[1]:
									print(bcolors.WARNING+ ">           infringing statement: " + bcolors.OKBLUE + S[0].statement )
									print(bcolors.WARNING+ ">>            Operator in question: "  + bcolors.ENDC + S[0].operator)
									c1 = bcolors.FAIL if  not S[2] else bcolors.OKGREEN
									c2 = bcolors.FAIL if  S[2] else bcolors.OKGREEN
									print(bcolors.WARNING+ ">>>             Returned " + c1 + str(S[2]) + ", expected " +c2+str(not S[2]))
									print(bcolors.WARNING+ ">>>>              State "+str(S[1].id)+": " + bcolors.ENDC + str(S[1].getVariables()))