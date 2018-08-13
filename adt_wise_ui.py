import adt_wise_logic as logic
import os, copy
from cmd import Cmd

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
		self.object = copy.deepcopy(object)

		# Finds the object's type 
		self.ADTType = getADTTypeFromObjName(self.object.name)

		# Title text for the embedded prompt
		self.title = "{adt}: {name}.".format(adt=self.ADTType.title() , name=self.object.name)
		self.title += "\nType in a command, 'help' or 'exit'.\n"

		self.availableMethods = self.object.calls # List

		# Dictionary of prompts for a command {<cmd-name>: []}
		self.promptsInfo = self.object.getInputPrompts()

		# Whether or not pointers need to be parsed
		self.usesPointers = self.object.usesPointers

		self.keyForPrompt = ":>>"

		# Set refresher function
		self.object.refresh = self.refresherPrompt

	def internalLoop(self):
		while True:

			# Embedded prompt is displayed
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
							print(parse(response))

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
								print(errorMessage)
								
								count += 1

								if count >= 3:
									print("You have responded incorrectly 3 times. Exiting prompt...")
									limitExceeded = True
									break

						if limitExceeded:
							break

					if not limitExceeded: # If evrything is valid
						# GUI needs another thread to run this
						response = funcToRun(**kwargs)

						clear()

						if response:
							print(parse(response))

						input("Press enter to continue... ")
						clear()


			elif cmd == "help":
				print(self.object.__doc__())
				print("For current purposes, the available commands are:\n")

				for callName in self.availableMethods:

					# Casing the print right
					thisCommand = callName.title()
					
					# Reading command info from docstring
					info = self.obj.getMethod(thisCommandi).__doc__ or '' 

					print(thisCommand + "\n\t" + info)

				input("Press enter to continue...")

			elif cmd == "exit":
				print("Saving modifications...")
				print("Exiting ADT interface.")
				break

			else:
				print("The command '{}' is not valid.".format(cmd))
				print("Check spelling, type 'help' for instructions.")

	def embeddedPrompt(self):
		"""The internal prompt which is used when handling an object which can be invoked from with adt 
		Parameters: Text to be displayed as title, The object to be used for display"""

		clear()

		print(self.title)		
		self.displayValuesWithinADT()

		if self.usesPointers:
			print()
			self.displayPointersWithinADT()

		print()

	def displayValuesWithinADT(self):
		# Returns a list [ {<heading>: {<attr>: <val>, } }, ]
		obj = self.object

		numberOfHeadings = len(obj.dataItems)

		padding = "    "
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
				parametersForRows[heading] = retrfunc(nodeIndex)
				parametersForRows["Index"] = nodeIndex

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

			pointerValue = self.object.getSpecialPointersValue(pointer)

			parametersForRows = {"PointerName": pointerName, "Value": pointerValue}
			print(placeholderTemplate.format(**parametersForRows))
		
		print(demarc)

	def refresherPrompt(self):
		if self.skipThroughPostings: # If post should be short-circuited
			return None

		clear()

		self.embeddedPrompt()

		logString = parse(self.object.log)
		print(logString)

		self.object.resetLog()

		input("Press enter to continue... ")

class adt_wise_ui(Cmd):
	# def __init__

	maxNumOfPrompts = 3

	availableADTTypes = logic.getavailableADTCallNames()
	existingObjects = logic.fetchAllADTObjNames()

	maxNumOfNodes = 12
	minNumOfNodes = 3

	maxPermissibleLengthOfName = 15

	def do_load(self, args):
		"""Loads an existing ADT for use."""

		if args:
			nameOfObj = args
		else:
			nameOfObj =  input("Enter the name (Case-Sensitive) of the ADT to load. :> ")

		objNames = logic.fetchAllADTObjNames()

		if nameOfObj not in objNames:
			print("An object with that name does not exist.")

		else:
			objToUse = logic.retrieveADTObjectByName(nameOfObj)

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
			for objName in self.existingObjects:

				typeOfObj = getADTTypeFromObjName(objName)

				row = placeholderTemplate.format(ADTName = objName, ADTType = typeOfObj)
				print(row)

		print(demarc)
		
	def validTypeOfADT(self, typeOfADT):
		"""If valid returns True, else returns an error message """

		if typeOfADT.lower().strip() in self.availableADTTypes:
			return True
		else:
			return "{} is not a supported type of ADT. Choose one from the available types.".format(typeOfADT)

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
		else:
			return("Please provide a integer between {min} and {max}.".format(min = self.minNumOfNodes,
			max = self.maxNumOfPrompts))

	def do_create(self, args):
		"""Allows for creating a new ADT."""

		limitExceeded = False
		invalidEntry = False

		# Process argument to split on ',' and strip elements of trailing/leading spaces

		arguments = args.split(",")
		arguments = list(map(lambda x: x.strip(), arguments))

		if arguments == ['']: # If no arguments received

			# Prompts for ADT Type
			if not limitExceeded:
				for i in range(self.maxNumOfPrompts):

					print("The following types of ADT are available:\n")
					for ADTType in self.availableADTTypes:
						typeOfADT = ADTType.title()

						print("{type:>4}".format(type=typeOfADT) )

					# typeOfADT
					typeOfADT = input("\nWhat type of ADT do you want to make? ")

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
			if not limitExceeded:
				for i in range(self.maxNumOfPrompts):
					# name
					name = input("What do you want to name this ADT? ").strip()

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
			if not limitExceeded:
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
				invalidEntry = True

		elif len(arguments) == 3: # If 3 arguments received

			typeOfADT, name, nodeCount = arguments

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

		else:
			invalidEntry = True
	
		# Build ADT or give error message
		if not invalidEntry:
			# ADT Call names are stored in lower-case
			typeOfADT = typeOfADT.lower().strip()

			logic.createADT(name, typeOfADT, nodeCount)
			self.existingObjects = logic.fetchAllADTObjNames()

		elif len(arguments) not in [0, 3]:
			print("Either provide no arguments or exactly 3 valid ones seperated by commas.")

def start():
	promptLoop = adt_wise_ui()
	promptLoop.prompt = ":>> "

	header = "...Starting"
	header += "\n" + "Type 'help' to list available commands."
	header += "\n" + "Type 'help' followed by command name for additional info on a command." 
	header += "\n"

	promptLoop.cmdloop(header)

if __name__ == "__main__":
	start()


