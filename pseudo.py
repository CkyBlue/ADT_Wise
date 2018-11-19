class PseudoCode:
	def __init__(self):
		""""A list of strings, each string is a seperate line,	the list is prepared by the extract method
			One additional 0 index entry is added in the beginning of the statements fetched by extract.
			This is to indicate invalid attempts to change statement activity
			For eg, if indices go upto 15 statements and someone attempts to change activity
			for index 17, the change shows for index 0
			Activity means on or off, active statements are those that
			are highlighted, each entry in the statements has an on or off propertry associated with it

			The additional 0 index entry also ensures that the line-numbers that show up in text-editors
			for the pseudocode text which start from 1 match the statement's index here

			Index 0 cannot be made active like the other indices can be since it is an error flag

			Activate means set activity to True for corresponding entry
			"""

		# Each entry is going to be a dictionary with the keys 'statement' and 'activity'
		self.statements = [{"statement": "", "activity": False}] # Index 0 that is automatically added
		self.length = 1

	def extract(self, text):
		statements = text.split("\n")

		# Overwrite
		self.statements = [{"statement": "", "activity": False}] # Index 0 that is automatically added
		self.length = 1

		for statement in statements:
			self.length += 1
			self.statements.append({"statement": statement, "activity": False})

	def highlight(self, indices):
		# Parameter indices is a list of index values for which statements need to be highlighted

		self.deactivateAll()

		for index in indices: # For each index
			if str(index).isdigit(): # If it is a number value
				self.activate(int(index)) # Try to activate it

	def deactivateAll(self):
		for statement in self.statements:
			statement["activity"] = False

	def activate(self, index):
		# Activate the entry at a particular index
		if index > self.length - 1: # If index invalid
			self.statements[0]["activity"] = True

		else:
			if index != 0: # If index is not 0, only then set is as active
				self.statements[index]["activity"] = True
