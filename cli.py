from actions import Null, CallableActions, Prompts, PseudoCode
import os

def parse(logTexts):
	"""Takes a list and gives a string where the items are indivisual statements,"""
	logString = ""

	for statement in logTexts:
		logString += statement + "\n"

	return logString

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

class CLI_Actions(CallableActions):
	def lock(self):
		self.lockCallBack(self.logTexts)
		self.logTexts = []

		input("Press Enter to continue...")
		clear()

	def executeAssociatedFunction(self, promptedValues):
		#any function to be freezed must expect keyword arguments lock and log

		promptedValues["lock"] = self.lock
		promptedValues["log"] = self.log
		promptedValues["light"] = self.light

		self.processing = True
		self.locked = True

		#the dictionary is ** operated to turn dictionary key into key arguments
		#thus valueName in the Prompts object should match variable names anticipated by function to execute

		self.functionWrapper(**promptedValues)

class CLI_Controller:
	def __init__(self, source):
		self.source = source(lockCallBack = self.lockCallBack, 
			actionEndTarget = self.endTarget)

		self.displays = []
		self.configureDisplay()

		self.pseudoCode = PseudoCode()

		self.actions = {}

		self.keyPrompt = ":>> "

		for action in self.source.getActions():
			name = action.name.lower()
			self.actions[name] = action

	def configureDisplay(self):
		# Reads source to find if data table (data property), variable table (variables property)
		# and pointer table (pointers property) exist

		source = self.source

		# Each item at dataObjs is associated with an item at allDisplays with the same index pos
		dataObjs = [source.data, source.variables, source.pointers]
		allDisplays = [self.displayDataTable, self.displayVariables, self.displayPointers]

		# If anyone one of the attributes in the dataObjs list are not defined in the source class
		# They will take the None value assigned at the base Operations class
		for index in range(len(dataObjs)):
			dataObj = dataObjs[index]

			# If a particular data object is defined (not None), register the function used to
			#  display it as one of those to be used by display()
			if dataObj != None:
				self.displays.append(allDisplays[index])

	def display(self):
		for displayFunc in self.displays:
			displayFunc()

	def displayPseudoCode(self):
		pseudo = self.pseudoCode

		print("Pseudocode: \n")
		for i in range(pseudo.length):
			activity = pseudo.statements[i]["activity"]
			statement = pseudo.statements[i]["statement"]

			lineCount = "{:0>3}".format(i) 

			prefix = suffix = ""

			if activity:
				prefix = "*"
				suffix = ""

			representation = "{p:^3} {lc} {st} {s}".format(p = prefix, lc = lineCount, st = statement,	s = suffix)

			print(representation)
		print()

	def displayDataTable(self):
		padding = 12

		# Add automsted index

		itemNames = list(self.source.data.data.keys())
		
		itemNamesdisplay = self.getFormattedRow(itemNames, padding)
		demarc = "-" * len(itemNamesdisplay)

		print(demarc + "\n" + itemNamesdisplay + "\n" + demarc)

		for index in range(self.source.data.size):
			items = []
			for item in itemNames:
				items.append(self.source.data.getValue(item, index))

			print(self.getFormattedRow(items, padding)) 

		print(demarc)

	def displayVariables(self):
		padding = 30

		variableNames = list(self.source.variables.data.keys())
		
		itemsdisplay = self.getFormattedRow(["Variables", "Value"], padding)
		demarc = "-" * len(itemsdisplay)

		print(demarc + "\n" + itemsdisplay + "\n" + demarc)

		for variable in variableNames:
			item = self.source.variables.getValue(variable)
			print(self.getFormattedRow([variable, item], padding)) 

		print(demarc)

	def displayPointers(self):
		padding = 30

		pointerNames = list(self.source.pointers.data.keys())
		
		itemsdisplay = self.getFormattedRow(["Pointers", "Value"], padding)
		demarc = "-" * len(itemsdisplay)

		print(demarc + "\n" + itemsdisplay + "\n" + demarc)

		for pointer in pointerNames:
			item = self.source.pointers.getValue(pointer)
			print(self.getFormattedRow([pointer + " Pointer", item], padding)) 

		print(demarc)

	def getFormattedRow(self, items, padding):
		"""Takes in a list (items) and an integer (padding)

		for list ['Item', 'Val', 'Ptr'] and padding of 4,
		returns the string '|Item| Val| Ptr|'

		The gap between '|'s contains <padding> no. of characters (w/ spaces for padding)
		If string in list is too long, the first <padding> no. of characters show up
		"""

		items = list(map(lambda x: str(x)[:padding], items))
		placeholder = "|"

		for i in range(len(items)):
			placeholder += "{:^" + str(padding) + "}|"

		return placeholder.format(*items)

	def displayAvailableActions(self):
		padding = 30
		
		itemsdisplay = self.getFormattedRow(["Available Operations"], padding)
		demarc = "-" * len(itemsdisplay)

		print(demarc + "\n" + itemsdisplay + "\n" + demarc)

		count = 1
		# Eventually integrate accessing Commands through ID

		for action in self.actions.keys():
			name = action.title()
			print(self.getFormattedRow([name], padding)) 

			count += 1

		print(demarc)

	def displayHeader(self):
		print("Enter 'run' to see all available actions or 'exit' to quit.")

	def loop(self):
		while True:
			clear()
			self.displayHeader()
			self.display()

			userInput = input(self.keyPrompt)

			# "CMD" -> "cmd"
			cmd = userInput.lower()

			if cmd == "run":
				self.displayAvailableActions()

				print("Type the name of the action to run.")
				actionNameInput = input().lower()

				for actionName in self.actions.keys():
					if actionName == actionNameInput.lower():
						actionObj = self.actions[actionName]

						promptedValues = {}

						for prompt in actionObj.prompts:
							print(prompt.promptMsg+":")
							
							inputValid = False

							while inputValid != True:
								userInput = input(self.keyPrompt)

								inputValid = errorMsg = prompt.validatorFunc(userInput)
								if inputValid != True:
									print(errorMsg)

								else:
									promptedValues[prompt.valueName] = userInput

						clear()
						self.pseudoCode = actionObj.codeObj
						actionObj.executeAssociatedFunction(promptedValues)
						clear()
						break

				else:
					print("Action {} is not recognized.".format(cmd))

			elif cmd == "exit":
				input("Press Enter to end program.")
				break
			else:
				print("Unknown command.")
			input("Press Enter to continue")

	def lockCallBack(self, logTexts):
		self.display()
		self.displayPseudoCode()
		print(parse(logTexts))

	def endTarget(self):
		print("Operation ended.")