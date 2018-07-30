import adt_wise_logic as logic
import os, copy
from cmd import Cmd

"""Status of 0 for errors that are expected and handled,
-1 for those that are unexpected.

Design a way to add undo: Develop the undo group
Develop argument pasrsing for create and load
Add a delete function

"""
	
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

def getADTType(obj):
	index = dict(logic.fetchIndex())

	for key in index.keys():
		if obj.getName() == key:
			return index[key]
			
	else:
		return None

class ADTObjectHandler:
	def __init__(self, object):
		"""Uses an ADT object which is input as parameter to build an embeded interface."""

		# ADT object
		self.__object = copy.deepcopy(object)

		# Finds the object's type 
		self.__ADTType = getADTType(self.__object)

		# Title text for the embedded prompt
		self.__title = "{adt}: {name}.".format(adt=self.__ADTType.title() , name=self.__object.getName())
		self.__title += "\nType in a command, 'help' or 'exit'.\n"

		self.__availableMethods = self.__object.getMethods() # Dictionary {<callName> : <function>}
		self.__methodCalls = self.__availableMethods.keys()

		# Dictionary of prompts for a command {<cmd-name>: []}
		self.__promptsInfo = self.__object.getInputPrompts()

		self.__availableADTs =  logic.getavailableADTs()

		# Whether or not pointers need to be parsed
		self.__usesPointers = self.__object.usesPointers

		self.__keyForPrompt = ":>>"

		# Set refresher function
		self.__object.setRefresher(self.refresherPrompt)

	def internalLoop(self):
		while True:

			# Embedded prompt is displayed
			self.embeddedPrompt()

			userInput = input("{} ".format(self.__keyForPrompt))

			# " CMD  now" -> "cmd"
			cmd = userInput.lower().split()
			if len(cmd) > 0:
				cmd = cmd[0] 
			else:
				cmd = ""

			# Evaluate input
			if cmd in self.__methodCalls:
				funcToRun = self.__availableMethods[cmd]

				# Checks the promptsInfo dictionary for a key with name matching the cmd.
				prompts = self.__promptsInfo.get(cmd, None)

				# If no values need to be prompted for a function
				if prompts == None:
					response = funcToRun()
					print(response, end = "")

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

							if valid:
								kwargs[keyName] = val
								break

							else:
								print(prompt["errorMsg"])
								count += 1

								if count >= 3:
									print("You have responded incorrectly 3 times. Exiting prompt...")
									limitExceeded = True
									break

						if limitExceeded:
							break

					if not limitExceeded: # If evrything is valid
						response = funcToRun(**kwargs)

						clear()
						print(parse(response) + "\n")
						input("Press enter to continue... ")
						clear()


			elif cmd == "help":
				print(obj.__doc__)
				print("For current purposes, the available commands are:\n")
				for command in methodCalls:

					# Casing the print right
					thisCommand = command.title()
					
					# Reading command info from docstring
					info = availableMethods[command].__doc__ or ''

					print(thisCommand + "\n\t" + info)

			elif cmd == "exit":
				print("Saving modifications...")
				print("Exiting ADT interface.")

			else:
				print("The command '{}' is not valid.".format(cmd))
				print("Check spelling, type 'help' for instructions.")

	def embeddedPrompt(self):
		"""The internal prompt which is used when handling an object which can be invoked from with adt 
		Parameters: Text to be displayed as title, The object to be used for display"""
		
		clear()

		print(self.__title)		
		self.displayValuesWithinADT()

		if self.__usesPointers:
			print()
			self.displayPointersWithinADT()

		print()

	def displayValuesWithinADT(self):
		# Returns a list [ {<heading>: {<attr>: <val>, } }, ]
		internals = self.__object.getOrganizedData() 

		numberOfHeadings = len(internals)

		padding = "    "
		widthForIndex = 15

		# Initially,
		placeholderTemplate = padding + "|"
		demarcLength = 1
		parametersForHeader = {}

		parametersForHeader = {"Index": "Index of Node"} # Header for index, index is imposed by the function
		placeholderTemplate += "{Index:^" + str(widthForIndex) + "}|"

		demarcLength += (widthForIndex + 1)

		for index in range(numberOfHeadings): 
			# Accumulates headings into template for placeholder
			# and sets up variables used for controlling output

			# Grabs the key of the list entry, there is only one key
			keyName = list(internals[index].keys())[0]

			width = internals[index][keyName]["width"] # Gets the width attribute

			placeholderTemplate += "{" + keyName + ":^" + str(width) + "}|"
			demarcLength += (width + 1)

			parametersForHeader[keyName] = keyName.title()

		demarc = padding + "-" * demarcLength

		print(demarc + "\n" + placeholderTemplate.format(**parametersForHeader) + "\n" + demarc)

		for nodeIndex in range(self.__object.numberOfNodes):	

			parametersForRows = {}

			# Builds a dictionary for formatting
			for headingCount in range(numberOfHeadings):

				# internal is set up as [ {<heading> : {<key>: <value>,} } ,],

				# Each outermost dictionary has only one key
				keyName = list(internals[headingCount].keys())[0]

				# The value to the header key is a dictionary consisting of properties: width and values
				parametersForRows[keyName] = internals[headingCount][keyName]["values"][nodeIndex]

				parametersForRows["Index"] = nodeIndex

			print(placeholderTemplate.format(**parametersForRows))

		print(demarc)
					
		########### The following will come in useful when making traversal

		# else: # If empty ADT, displays atleast one blank line.

		# 	# Builds a dictionary for formatting
		# 	for headingCount in range(numberOfHeadings):

		# 		# internal is set up as [ {<heading> : {<key>: <value>,} } ,],
		# 		# Each outermost dictionary has only one key

		# 		keyName = list(internals[headingCount].keys())[0]
		# 		# The value to the header key is a dictionary consisting of properties: width and values
		# 		parametersForRows[keyName] = ""

		# 		print(placeholderTemplate.format(**parametersForRows))/

	def displayPointersWithinADT(self):
		# Returns a list [{<Pointer Namw>: <Pointer Value> }, ]
		pointers = self.__object.getSpecialPointers() 

		numberOfPointers = len(pointers)

		padding = "    "
		widthForValues = 7

		# Initially,
		placeholderTemplate = padding + "|"
		demarcLength = 1

		extraSpaceToTheRight = 2

		# Makes a list out of length of pointer names and get's longest
		#									Pointer name  						List of dictionary with single keys
		maxLengthOfPointerName = max(len( list(pointer.keys())[0] ) for pointer in pointers) + extraSpaceToTheRight

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
			# Grabs the pointer name for the entry, there is only one key
			pointerName = list(pointer.keys())[0]

			pointerValue = pointer[pointerName]

			parametersForRows = {"PointerName": pointerName, "Value": pointerValue}
			print(placeholderTemplate.format(**parametersForRows))
		
		print(demarc)

	def refresherPrompt(self):
		clear()

		self.embeddedPrompt()

		logString = parse(self.__object.getLog())
		print(logString)

		self.__object.setLog([])

		input("Press enter to continue... ")

def fetchADTMethodsList():
	pass

typeOfADT = "queue"

class adt_wise_ui(Cmd):
	# def __init__

	maxNumOfPrompts = 3

	availableADTTypes = logic.getavailableADTs()
	existingObjects = logic.fetchIndex()

	maxNumOfNodes = 12
	minNumOfNodes = 3

	maxPermissibleLengthOfName = 15

	def do_load(self, args):
		"""Loads an existing ADT for use."""

		if args:
			nameOfObj = args
		else:
			nameOfObj =  input("Enter the name (Case-Sensitive) of the ADT to load. :> ")

		# dict( [[<key>, <value>], ] ) => {<key>: <value>, }
		objNames = dict( logic.fetchIndex() ).keys()

		if nameOfObj not in objNames:
			print("An object with that name does not exist.")

		else:
			objToUse = logic.retrieveObj(nameOfObj)

			# Creates an object handler for the object and runs the internal loop
			ADTObjectHandler(objToUse).internalLoop()

	def do_list(self, args):
		"""Lists all existing ADTs"""

		padding = "    "

		widthForADTName = self.maxPermissibleLengthOfName
		widthForADTType = 14

		placeholderTemplate = padding + "|"
		demarcLength = 1

		placeholderTemplate += "{ADTName:^" + str(widthForADTName) + "}|"
		demarcLength += 1 + widthForADTName 

		placeholderTemplate += "{ADTType:^" + str(widthForADTType) + "}|"
		demarcLength += 1 + widthForADTType

		header = placeholderTemplate.format(ADTName = "Name of ADT", ADTType = "Type Of ADT")

		demarc = padding + "-" * demarcLength
		
		print(demarc + "\n" + header + "\n" + demarc)

		if len(self.existingObjects) == 0:
			row = placeholderTemplate.format(ADTName = "", ADTType = "")
			print(row)
		else:
			for pair in self.existingObjects:

				objName = pair[0]
				typeOfObj = pair[1]

				row = placeholderTemplate.format(ADTName = objName, ADTType = typeOfObj)
				print(row)

		print(demarc)
		
	def validTypeOfADT(self, typeOfADT):
		"""If valid returns True, else returns an error message """

		if typeOfADT in self.availableADTTypes.keys():
			return True
		else:
			return "{} is not a supported type of ADT. Choose one from the available types.".format(typeOfADT)

	def validADTName(self, name):
		"""If valid returns True, else returns an error message """
		
		if name in dict( self.existingObjects ).keys():
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
		else:
			return("Please provide a integer between {min} and {max}.".format(min = self.minNumOfNodes,
			max = self.maxNumOfPrompts))

	def do_create(self, args):
		"""Allows for creating a new ADT."""

		limitExceeded = False

		arguments = args.replace(",", " ").split()

		if arguments == []: # If no arguments received

			# Prompts for ADT Type
			for i in range(self.maxNumOfPrompts):

				print("The following types of ADT are available:\n")
				for ADTType in self.availableADTTypes.keys():
					typeOfADT = ADTType.title()

					print("{type:>4}".format(type=typeOfADT) )

				# typeOfADT
				typeOfADT = input("\nWhat type of ADT do you want to make? ").lower().strip()

				# Validation
				valid =  self.validTypeOfADT(typeOfADT)

				if valid == True:
					break
				else:
					errorMsg = valid
					print(errorMsg)
			else:
				limitExceeded = True

			# Prompts for name
			for i in range(self.maxNumOfPrompts):
				# name
				name = input("What do you want to name this ADT? ")

				# Validation
				valid =  self.validADTName(name)

				if valid == True:
					break
				else:
					errorMsg = valid
					print(errorMsg)
			else:
				limitExceeded = True

			# Prompts for number of nodes
			promptText = "How many nodes do you want it to have? <{min}-{max}> ".format(min = self.minNumOfNodes, 
				max = self.maxNumOfNodes)
			
			for i in range(self.maxNumOfPrompts):
				# nodeCount
				nodeCount = input(promptText).strip()

				# Validation
				valid =  self.validNodeCount(nodeCount)

				if valid == True:
					break
				else:
					errorMsg = valid
					print(errorMsg)			
			else:
				limitExceeded = True

			if limitExceeded:
				print("You have responded incorrectly 3 times. Exiting prompt...")
			else:
				logic.createADT(name, typeOfADT, nodeCount)
				self.existingObjects = logic.fetchIndex()

		elif len(arguments) == 3:

			typeOfADT, name, nodeCount = arguments
			typeOfADT = typeOfADT.lower().strip()

			invalidEntry = False

			for value, validator in [[typeOfADT, self.validTypeOfADT],
				[name, self.validADTName],
				[nodeCount, self.validNodeCount]
			]:
				valid =  validator(value)

				if valid == True:
					continue
				else:
					errorMsg = valid
					print(errorMsg)	

					invalidEntry = True
	
		if not invalidEntry:
			logic.createADT(name, typeOfADT, nodeCount)

			self.existingObjects = logic.fetchIndex()

		else:
			print("Either provide no arguments or exactly 3 valid ones seperated by spaces.")

promptLoop = adt_wise_ui()
promptLoop.prompt = ":>> "

header = "...Starting"
header += "\n" + "Type 'help' to list available commands."
header += "\n" + "Type 'help' followed by command name for additional info on a command." 
header += "\n"
 
promptLoop.cmdloop(header)

# Expand to allow accessing through IDs generated on UI layer

