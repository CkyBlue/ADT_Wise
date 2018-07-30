"""Methods that need to avilable for access through call names
need to be appended appropriately to the getMethods function.

If the function needs arguments, the prompt, validator and error-message need
to be served through the getInputPrompts function.

Each function shows its working through a log
Information is added to the log through the function self.post(<Info-String>)
Each time self.__refresh, or rfr in the short-hand form, is fired the info in the log is displayed

The return is a list of strings
it serves as the response message
It is handled somewhat differently from logs

The action detailed in the log should fire after the refresh so that 
changes mentioned are only observed when pressing enter brings the
next refresh and user can follow the change more easily by 
knowing where to look 

The info that shows up through 'help <command-name>'
is the doc-string, the text in the triple quotation mark comments  
"""

### Note to self: Pad IDs in organized data return

class Record:
	def __init__(self):
		self.idCol = ""
		self.data = ""

class HashTable:
	def __init__(self, name, length):
		self.__name = name
		self.numberOfNodes = int(length)

		self.recordArray = [Record() for i in range(self.numberOfNodes)]
		self.initializeId(self.recordArray)

		self.__refresh = (lambda: None)
		self.usesPointers = False
		self.__log = []


	def initializeId(self, obj): # Set all IDs initially to 0
		for index in range(len(obj)):
			obj[index].idCol = 0

	def __doc__(self):
		### Add elaboration through other string items added to the list
		### Each seperate entry prints on a different line

		text = ["A hash table is an abstract data type",
		"Add more elaboration later..."
		]

		output = ""

		for i in text:
			if i != (len(text) - 1) :
				output += i + "\n"
			else:
				output += i

		return output

	def setLog(self, newLog):
		self.__log = newLog

	def getLog(self):
		return self.__log

	def setRefresher(self, func):
		self.__refresh = func

	def setName(self, name):
		self.__name = name

	def getName(self):
		return self.__name

	def getInputPrompts(self):
		"""Returns data that allows the user interface to send data properly to functions that need arguments"""

		prompts = {}

		# The dictionary is inside an array so that if a single command need multiple values, the existing system permits
		# valueName must match the name of the parameter for the function

		prompts["insert"] = [

		# Prompt for ID
		{"promptMsg": "Enter item ID", 

		"validator": lambda x: x.isdigit() and x <= "9999" and x >= "0", # Anonymous func for validation
		"errorMsg": "The ID must be numbers only \nand between 0 to 9999.",

		"valueName": "idForNewEntry"
		},

		# Prompt for value
		{"promptMsg": "Enter item to be inserted",

		"validator": lambda x: len(x) <= 20 and x.replace(" ", "").isalnum(), # Anonymous func for validation
		"errorMsg": "The item must be shorter than 20 letters, \nand aside from spaces must contain only alpha-numeric characters.",
		
		"valueName": "dataForNewEntry"
		}
		]

		prompts["search"] = [
		{"promptMsg": "Enter item to be inserted", 
		"validator": lambda x: True, # No validation needed
		"errorMsg": "The item must be shorter than 20 letters, \nand aside from spaces must contain only alpha-numeric characters.",
		"valueName": "itemToBeSearched"
		}
		]

		prompts["remove"] = [
		{"promptMsg": "Enter the ID of the entry you wish to remove", 
		"validator": lambda x: True, #
		"errorMsg": "The ID can be numbers only \nand between 0 to 9999.",
		"valueName": "idOfItemToBeRemoved"
		}
		]

		return prompts

	def __str__(self):
		return self.__name

	def insert(self, idForNewEntry, dataForNewEntry):

		msg = []

		# Short-hand
		post = self.post
		rfr = self.__refresh

		index = self.hash(idForNewEntry)

		currentPointer = index
		tableFull = False

		while not tableFull and self.recordArray[currentPointer].idCol != 0: # Exhaust table

			# Move to next position
			currentPointer += 1

			# If wrapping around needed
			if currentPointer >= len(self.recordArray):
				currentPointer = 0

			# If the current pointer wraps back to initial position
			if currentPointer == index:
				tableFull = True

		if tableFull:
			msg.append("The item could not be added as the table is full.")

		else:

			self.recordArray[currentPointer].idCol = idForNewEntry
			self.recordArray[currentPointer].data = dataForNewEntry

			msg.append("The item was added successfully at index {}".format(currentPointer))

	def remove(self, idOfItemToBeRemoved):

		if idForNewEntry.isdigit():
			index = self.hash(idForNewEntry)
			pointer = index
			noRecord= False
			while not noRecord and idForNewEntry != self.recordArray[pointer].idCol:
				pointer += 1
				if pointer >= len(self.recordArray):
					pointer = 0
				if pointer == index:
					noRecord = True
			if noRecord:
				print("No matching record found!")
			else:
				self.recordArray[pointer].data = ""
				self.recordArray[pointer].idCol = "0000"
				print("Entry removed!")

	def search(self, idForNewEntry):
		if idForNewEntry.isdigit():
			index = self.hash(idForNewEntry)
			pointer = index
			tableExausted = False
			while not tableExausted and idForNewEntry != self.recordArray[pointer].idCol:
				pointer += 1
				if pointer >= len(self.recordArray):
					pointer = 0
				if pointer == index or self.recordArray[pointer].data == "":
					tableExausted = True
			if not tableExausted:
				print("Record found at index {}".format(pointer))
			else:
				print("No matching entry found!")


	def hash(self, key):
		key = int(key)
		return key % self.numberOfNodes # Gives modulus appropriate to number of nodes

customers = HashTable(10)
while True:
	query = input("Enter query:> ")
	if query.lower() == "exit":
		break
	elif query.lower() == "show":
		print()
		demarc = "-"*48
		print(demarc)
		print("|{:^10} | {:^10} | {:^20}|".format("Index", "Id", "Item"))
		print(demarc)
		for index in range(len(customers.recordArray)):
			print("|{index:^10} | {id:^10} | {item:^20}|".format(index = ""+ str(index) + "", 
				id = customers.recordArray[index].idCol,
				item = customers.recordArray[index].data))
		print(demarc, "\n")
	else:
		queries = query.split(":")
		data = queries[-1].strip()
		cmd = queries[0].strip().lower()
		if cmd == "insert":
			items = data.split(",")
			if len(items) != 2:
				print("Insert two items, a ID and the data to be stored, seperated by a ','.")
			elif not items[0].strip().isdigit():
				print("IDs must be a number")
			else:
				idEntry = "{:0>4}".format(items[0])[-4:]
				dataEntry = items[1]
				customers.insert(idEntry, dataEntry)
		elif cmd == "remove":
			items = data.split(",")
			if len(items) > 1:
				print("Enter only the ID.")
			elif not items[0].strip().isdigit():
				print("IDs must be a number")
			else:
				idEntry = "{:0>4}".format(items[0])[-4:]
				customers.remove(idEntry)	
		elif cmd == "search":
			items = data.split(",")
			if len(items) > 1:
				print("Enter only the ID.")
			elif not items[0].strip().isdigit():
				print("IDs must be a number")
			else:
				idEntry = "{:0>4}".format(items[0])[-4:]
				customers.search(idEntry)
		else:
			print("Enter a valid command!")	