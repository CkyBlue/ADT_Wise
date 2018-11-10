class DataStructure:
	"""Takes strings (Eg: 'id', 'pointer') as parameters and uses them as keys
		keyword parameter size defines how long the list associated with each key is
		keywor parameter name is the name of the data strcture
		get/setValue methods take parameters key name (Eg: 'id', 'pointer') and index to access value
		setValue takes additionally the value to be set to
	"""

	def __init__(self, *args, **kwargs):

		self.data = {} #Dictionary where each item (Eg: 'id', 'pointer') is a key to an list 
		self.size = kwargs["size"] #Length of each list
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

dummyData = DataStructure("ID", "Value", "Pointer", size = 12, name = "Dummy")

for i in range(12):
	dummyData.setValue("ID", i, str(i))
	dummyData.setValue("Value", i, "Ram" + str(i))
	dummyData.setValue("Pointer", i, str(i + 1))
