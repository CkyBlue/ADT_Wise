class DataStructure:
	def __init__(self, *args, **kwargs):

		self.data = {} #Dictionary where each item (Eg: 'id', 'pointer') is a key to an list 
		self.size = kwargs["size"] #Length of each list

		for arg in args: # For each arg create a list
			self.data[arg] =  [''] * self.size #Create a list of appropriate length
				# and an associated entry in the dictionary with the arg as the key name

	def getValue(self, key, index): 
		"""Retrieves value by referring to the item name (Eg: 'id', 'pointer') and index"""

		return self.data[key][index]

	def setValue(self, key, index, value):
		"""Allows setting value by referring to the item name (Eg: 'id', 'pointer') and index"""

		self.data[key][index] = value

if __name__ = "__main__":

	QueueData = DataStructure("ID", "Value", "Pointer", size = 12)

	for i in range(12):
		QueueData.setValue("ID", i, "Ram" + str(i))

	for i in range(12):
		X = QueueData.getValue("ID", i)
		print(X)