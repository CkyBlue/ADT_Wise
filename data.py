"""These classes are used to store data, DataStructure tracks using indices in addition to keys 
(e.g item=>'Left Pointer', index=>"6")

VariableData and PointerData rely only on keys

Instead having too many methods: getLeftPointer, getIndex, etc
A single get/set pair is used with keys, and indices if applicable  

These form the source for many box widgets
"""

class DataStructure:
	"""Takes a list of strings (Eg: ['ID', 'Pointer']) as parameters and uses the strings as keys
		keyword parameter size defines how long the list associated with each key is
		keywor parameter name is the name of the data strcture

		get/setValue methods take parameters key name (Eg: 'id', 'pointer') and index to access value
		setValue takes additionally the value to be set to
	"""

	def __init__(self, args, **kwargs):

		self.data = {} #Dictionary where each item (Eg: 'id', 'pointer') is a key to an list 
		
		self.default_size = 12 #If size parameter (look below) is missing

		#For the size that is used for each list maintained by the DataStructure object to store data
		if "size" in list(kwargs.keys()): 
			self.size = kwargs["size"] 

		else: # Default size
			self.size = self.default_size

		self.keys = args #Keys to self.data
		self.name = kwargs["name"]

		for arg in args: # For each arg create a list
			self.data[arg] =  [''] * self.size #Create a list of appropriate length
				# and an associated entry in the dictionary with the arg as the key name

	def getValue(self, key, index): 
		"""Retrieves value by referring to the item name (Eg: 'id', 'pointer') and index"""

		return self.data[key][index]

	def setValue(self, key, index, value):
		"""Allows setting value by referring to the item name (Eg: 'id', 'pointer') and index"""

		self.data[key][index] = value

class VariableData:
	"""Behaves in a way similar to DatStructure"""
	def __init__(self, args, **kwargs):
		self.data = {} #Dictionary where each variable name is a key to its value 

		self.keys = args #Keys to self.data

		for arg in args: # For each arg
			self.data[arg] =  "" #Create an entry in the dictionary with the arg as key and "" as value

	def getValue(self, key): 
		"""Retrieves value by referring to the variable name and index"""

		return self.data[key]

	def setValue(self, key, value):
		"""Allows setting pointer value by referring to the variable type"""

		self.data[key] = value

class PointerData(VariableData):
	def __init__(self, args, **kwargs):
		super(PointerData, self).__init__(args, **kwargs)

		for arg in args: # For each arg
			self.data[arg] =  "-1"