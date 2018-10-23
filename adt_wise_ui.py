import adt_wise_logic as logic
import os, copy
from cmd import Cmd
from colorama import init, Style, Fore, Back
init()

color_mapping = {-1: Back.BLACK,
	0: Back.BLUE + Fore.WHITE,
	1: Back.CYAN + Fore.WHITE,
	2: Back.GREEN + Fore.WHITE,
	3: Back.MAGENTA + Fore.WHITE,	
	4: Back.RED + Fore.WHITE,
	5: Back.WHITE + Fore.BLACK,
	6: Back.YELLOW + Fore.BLACK}

header = "Type 'load' to choose an ADT to interact with, else type 'help' or 'exit'."  
header += "\n"

# Turn on for debugging purposes
noPosting = False

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

def parse(log):
	"""Takes a log list and gives a string where the items are indivisual statements,
	
	Consider developing to recognize markup
	"""
	content = ""

	for statement in log:
		content += statement + "\n"

	return content

def getADTTypeFromObjName(adtName):
	return logic.getADTTypeFromName(adtName)

class ADTObjectHandler:
	def __init__(self, object):
		"""Uses an ADT object which is input as parameter to build an embeded interface."""

		self.skipThroughPostings = noPosting

		# ADT object
		self.object = object

		# Title text for the embedded prompt
		self.title = "\nType in a command, 'help' or 'exit'.\n"

		self.availableMethods = self.object.calls # List

		# Dictionary of prompts for a command {<cmd-name>: []}
		self.promptsInfo = self.object.getInputPrompts()

		# Whether or not pointers need to be parsed
		self.usesPointers = self.object.usesPointers

		self.keyForPrompt = ":>>"

		# Set refresher function
		self.object.refresh = self.refresherPrompt

	def treeGraphic(self, obj, index):
		## To vary padding
		padding = 4

		widthOfItem = obj.dataItemsWidth["Item"]

		nodeFormat = "{index:^2}: |{left:^4}|{item:^" + str(widthOfItem) + "}|{right:^4}|"
		indexIndent = 4

		demarcUnit = "-"

		# Overlining demarcation
		demarcLength = 4 + widthOfItem + 4 + 4

		# and space for index preceder
		blockLength = demarcLength + indexIndent
		overline = " " * indexIndent + demarcUnit * demarcLength

		pad = " " * padding

		blankNode = nodeFormat.format(index = -1, left = "-", right = "-", item = "-")
		##
		currentNode = index

		if currentNode != -1:
			leftNode = obj.nodeArray[index].leftPointer
			rightNode = obj.nodeArray[index].rightPointer	
			root = nodeFormat.format(index = index,
				left = leftNode,
				right = rightNode,
				item = obj.nodeArray[index].item)
		else:
			leftNode = -1
			rightNode = -1		
			root = blankNode		

		if leftNode != -1:
			left = nodeFormat.format(index = leftNode,
				left = obj.nodeArray[leftNode].leftPointer,
				right = obj.nodeArray[leftNode].rightPointer,
				item = obj.nodeArray[leftNode].item)
		else:
			left = blankNode

		if rightNode != -1:
			right = nodeFormat.format(index = rightNode,
				left = obj.nodeArray[rightNode].leftPointer,
				right = obj.nodeArray[rightNode].rightPointer,
				item = obj.nodeArray[rightNode].item)
		else:
			right = blankNode

		output = ""
		output += pad + "{:^70}".format("Current node:") + "\n"
		output += pad + "{:^70}".format(overline + " "*3) + "\n"
		output += pad + "{:^70}".format(root + " "*3) + "\n"
		output += pad + "{:^70}".format(overline + " "*3) + "\n"	
		output += pad + "{:^70}".format("|") + "\n"
		output += pad + "{:^70}".format("-"*34) + "\n"
		output += pad + "{:<35}{:>35}".format(" "*17 + "|", "|" + " "*17) + "\n"
		output += pad + "{:<35}{:>35}".format(overline, overline + " "*3) + "\n"	
		output += pad + "{:<35}{:>35}".format(left, right + " "*3) + "\n"
		output += pad + "{:<35}{:>35}".format(overline, overline + " "*3) + "\n"

		return output

	def internalLoop(self):
		while True:
			self.object.resetLog()

			clear()
			# Embedded prompt is displayed
			print(self.title)
			self.embeddedPrompt()

			userInput = input("{} ".format(self.keyForPrompt))

			# " CMD  now" -> "cmd"
			cmd = userInput.lower().split()
			if len(cmd) > 0:
				cmd = cmd[0] 
			else:
				cmd = ""

			# Evaluate input
			if cmd in self.availableMethods:
				funcToRun = self.object.getMethod(cmd)

				if funcToRun == None:
					print("Call registered without designated function.")
					continue

				# Checks the prompts info dictionary for a key with name matching the cmd.
				prompts = self.promptsInfo.get(cmd, None)

				# If no values need to be prompted for a function
				if prompts == None:

					# GUI needs another thread to run this
					response = funcToRun()
					
					if response:
							clear()
							print(parse(response))

							input("Press enter to continue... ")
							clear()

				else: # If values need to prompted for

					kwargs = {} # Holds parameters that are to be passed into function that is to be fired.
					# kwargs is unpackaged into the function

					limitExceeded = False
					
					for prompt in prompts: # Uses prompt parameters to fetch values
						keyName = prompt["valueName"]

						count = 0

						while True: 
							val = input("{} :> ".format( (prompt["promptMsg"]) ) )

							valid = prompt["validator"](val)

							if valid == True: # If validator return True
								kwargs[keyName] = val
								break

							else: # Validator returns error message

								errorMessage = valid
								print("\n"+errorMessage)
								
								count += 1

								if count >= 3:
									print("You have responded incorrectly 3 times. Exiting prompt...")
									input("\nPress enter to continue... ")
									limitExceeded = True
									break

						if limitExceeded:
							break

					if not limitExceeded: # If evrything is valid
						response = funcToRun(**kwargs)

						clear()

						if response:
							print(parse(response))

						input("\nPress enter to continue... ")
						clear()

			elif cmd == "help":
				clear()
				print("Help:\n")
				print(self.object.__doc__())
				print("For current purposes, the available commands are:\n")

				for callName in self.availableMethods:

					# Casing the print right
					thisCommand = callName.title()
			
					# Reading command info from docstring
					info = self.object.getMethod(callName).__doc__ or '' 

					print(thisCommand + "\n\t" + info)

				toggleInfo = "Allows toggling the logs on or off."  
				print("Toggle" + "\n\t" + toggleInfo)

				input("\nPress enter to continue...")

			elif cmd == "exit":
				print("Exiting ADT interface.")

				input("Press enter to continue...")
				clear()
				break

			elif cmd == "toggle":
				self.skipThroughPostings = not self.skipThroughPostings

				translation = {True: "off", False: "on"} # Maps true->off, false->on
				print("Toggled postings to {}.".format(translation[self.skipThroughPostings])) # on/off

				input("\nPress enter to continue...")

			else:
				print("The command '{}' is not valid.".format(cmd))
				print("Check spelling, type 'help' for instructions.")

				input("\nPress enter to continue...")
	
	def embeddedPrompt(self):
		"""The internal prompt which is used when handling an object which can be invoked from with adt 
		Parameters: Text to be displayed as title, The object to be used for display"""

		self.displayValuesWithinADT()

		if self.usesPointers:
			print()
			self.displayPointersWithinADT()

		print()

	def displayValuesWithinADT(self):
		# Returns a list [ {<heading>: {<attr>: <val>, } }, ]
		obj = self.object

		numberOfHeadings = len(obj.dataItems)

		padding = " "*4
		widthForIndex = 15

		# Initially,
		placeholderTemplate = padding + "|"
		demarcLength = 1
		parametersForHeader = {}

		parametersForHeader = {"Index": "Index of Node"} # Header for index, index is imposed by the function
		placeholderTemplate += "{Index:^" + str(widthForIndex) + "}|"

		demarcLength += (widthForIndex + 1)

		for heading in obj.dataItems: 
			# Accumulates headings into template for placeholder
			# and sets up variables used for controlling output

			keyName = heading
			width = obj.dataItemsWidth[heading]

			placeholderTemplate += "{" + keyName + ":^" + str(width) + "}|"
			demarcLength += (width + 1)

			parametersForHeader[keyName] = keyName.title()

		demarc = padding + "-" * demarcLength

		print(demarc + "\n" + placeholderTemplate.format(**parametersForHeader) + "\n" + demarc)

		for nodeIndex in range(obj.numberOfNodes):	

			parametersForRows = {}

			# Builds a dictionary for formatting
			for heading in obj.dataItems:

				# Returns function which processes value fetching for a certain node index
				retrfunc = obj.dataItemsRetrievingFunc[heading]

				if "pointer" in heading.lower(): # Color Formatting
					n = retrfunc(nodeIndex)
					width = obj.dataItemsWidth[heading]
					parametersForRows[heading] =  color_mapping[n]
					parametersForRows[heading] += ("{:^" + str(width) + "}").format(str(n)) + Style.RESET_ALL

				else:
					parametersForRows[heading] = retrfunc(nodeIndex)

				i = nodeIndex
				parametersForRows["Index"] = color_mapping[i]
				parametersForRows["Index"] += ("{:^" + str(widthForIndex) + "}").format(str(i)) + Style.RESET_ALL

			print(placeholderTemplate.format(**parametersForRows))

		print(demarc)
					
	def displayPointersWithinADT(self):
		pointers = self.object.getSpecialPointersName() # List

		numberOfPointers = len(pointers)

		padding = "    "
		widthForValues = 10

		# Initially,
		placeholderTemplate = padding + "|"
		demarcLength = 1

		extraSpace = 2

		# Makes a list out of length of pointer names and get's longest
		maxLengthOfPointerName = max([len(pointer) for pointer in pointers]) + extraSpace

		# Demarcation length
		demarcLength += (widthForValues + 1)
		demarcLength += (maxLengthOfPointerName + 1)

		placeholderTemplate += "{PointerName:^" + str(maxLengthOfPointerName) + "}|"
		placeholderTemplate += "{Value:^" + str(widthForValues) + "}|"

		demarc = padding + "-" * demarcLength

		# Header
		print(demarc + "\n" + placeholderTemplate.format(PointerName="", Value="Values") + "\n" + demarc)

		# Body
		for pointer in pointers: 
			# Grabs the pointer name for the entry
			pointerName = pointer

			rawVal = self.object.getSpecialPointersValue(pointer)

			r = rawVal
			pointerValue = color_mapping[r]
			pointerValue += ("{:^" + str(widthForValues) + "}").format(str(r)) + Style.RESET_ALL

			parametersForRows = {"PointerName": pointerName, "Value": pointerValue}
			print(placeholderTemplate.format(**parametersForRows))
		
		print(demarc)

	def refresherPrompt(self):
		if self.skipThroughPostings: # If post should be short-circuited
			return None

		clear()

		self.embeddedPrompt()

		if self.object.hasTree: # If a tree graphic is required
			tree = self.treeGraphic(self.object, self.object.currentPointer)
			print(tree)

		logString = parse(self.object.log)
		print(logString)

		self.object.resetLog()
		input("Press enter to continue... ")
		for i in range(100):
			pass

class adt_wise_ui(Cmd):
	# initialization

	maxNumOfPrompts = 3

	availableADTTypes = logic.getAvailableADTCallNames()

	nodeCount = 7

	maxPermissibleLengthOfName = 15
		
	def validTypeOfADT(self, typeOfADT):
		"""If valid returns True, else returns an error message """

		if typeOfADT.lower().strip() in self.availableADTTypes:
			return True
		else:
			return "{} is not a supported type of ADT. Choose one from the available types.".format(typeOfADT)

	def do_help(self, args):
		print("For current purposes, the available commands are:\n")

		availableCommands = ["load", "exit"]
		ascMethods = {"load": self.do_load, "exit": self.do_exit}

		for cmd in availableCommands:
			# Casing the print right
			thisCommand = cmd.title()
	
			# Reading command info from docstring
			info = ascMethods[cmd].__doc__ or ''

			print(thisCommand + "\n\t" + info)
	
	def validADTName(self, name):
		"""If valid returns True, else returns an error message """
		
		if name in self.existingObjects:
			return("An ADT with ths name already exists. Try another name.")

		elif len(name) > self.maxPermissibleLengthOfName:
			return("The name should be shorter than {} letters.".format(self.maxPermissibleLengthOfName))

		elif not name.isalnum():
			return("The name must only contain alpha-numeric characters. Spaces are not allowed.")

		else:
			return True

	def validNodeCount(self, nodeCount):
		"""If valid returns True, else returns an error message """

		if nodeCount.isdigit():
			nodeCount = int(nodeCount)
			if nodeCount >= self.minNumOfNodes and nodeCount <= self.maxNumOfNodes:
				return True
		return ("Please provide a integer between {min} and {max}.".format(min = self.minNumOfNodes,
			max = self.maxNumOfNodes))

	def do_load(self, args):
		"""Loads a particular type of ADT for interacting with."""

		limitExceeded = False
		invalidEntry = False

		# Process argument to split on ',' and strip elements of trailing/leading spaces

		arguments = args.split(",")
		arguments = list(map(lambda x: x.strip(), arguments))

		if arguments == ['']: # If no arguments received

			# Prompts for ADT Type
			for i in range(self.maxNumOfPrompts):
				print("The following types of ADT are available:\n")

				self.displayAvailableADTs()

				# typeOfADT
				typeOfADT = input("\nWhat type of ADT do you want to load? ")

				# Validation
				valid =  self.validTypeOfADT(typeOfADT)

				if valid == True:
					break
				else:
					errorMsg = valid
					print(errorMsg)
			else:
				limitExceeded = True

			if limitExceeded:
				print("You have responded incorrectly 3 times. Exiting prompt...")
				invalidEntry = True

		elif len(arguments) == 1: # If 1 arguments received

			typeOfADT = arguments[0]

			valid =  self.validTypeOfADT(typeOfADT)

			if valid != True:
				errorMsg = valid
				print(errorMsg)	
				invalidEntry = True

		else:
			invalidEntry = True
	
		# Build ADT or give error message
		if not invalidEntry:
			# ADT Call names are stored in lower-case
			typeOfADT = typeOfADT.lower().strip()

			# Create and Load 
			adtClass = logic.getADTClassFromCallName(typeOfADT)
			objToUse = adtClass("Micro", self.nodeCount)
			ADTObjectHandler(objToUse).internalLoop()

			# Redisplay header after finished working with the object
			print(header)

		elif len(arguments) not in [0, 1]:
			print("Either provide no arguments or 1 valid one. You provided {}.".format(len(arguments)))

	def do_exit(self, args):
		"""Exits the program."""
		print("Exiting.")
		raise SystemExit

	def displayAvailableADTs(self):
		
		numberOfHeadings = 2
		padding = " "*4

		widthForCol = 20
		widthForIndex = 5
		keyName = "ADTs"

		# A template is made

		placeholderTemplate = padding + "|"
		demarcLength = 1

		# Values to be fed for header

		# Index
		parametersForHeader = {}
		parametersForHeader = {"Index": ""} # Header for index

		placeholderTemplate += "{Index:^" + str(widthForIndex) + "}|"

		demarcLength += (widthForIndex + 1)

		# ADTs
		placeholderTemplate += "{" + keyName + ":^" + str(widthForCol) + "}|"

		demarcLength += (widthForCol + 1)

		parametersForHeader[keyName] = keyName

		# Demarcation
		demarc = padding + "-" * demarcLength

		# Print header
		print(demarc + "\n" + placeholderTemplate.format(**parametersForHeader) + "\n" + demarc)

		ADTNames = list(logic.ADTS.keys())

		# Dump ADT names into template and print
		for i in range(len(ADTNames)):

			parametersForRows = {}
			# Builds a dictionary for formatting

			parametersForRows[keyName] = ADTNames[i].title()
			parametersForRows["Index"] = ("{:^" + str(widthForIndex) + "}").format(str(i + 1))

			print(placeholderTemplate.format(**parametersForRows))

		print(demarc)

def start():
	promptLoop = adt_wise_ui()
	promptLoop.prompt = ":>> "

	promptLoop.cmdloop("...Starting\n" + header)

if __name__ == "__main__":
	start()


