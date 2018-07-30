from time import sleep

class Node():
	
	def __init__(self, key, value):
		self.__value = value # value : string
		self.__key = key # key : string

	def SetKey(self, key):
		self.__key = key

	def GetKey(self):
		return self.__key

	def SetValue(self, value):
		self.__value = value

	def GetValue(self):
		return self.__value

class HashTable():

	def __init__(self, length):
		self.__nodeArray = [Node("", "") for i in range(length)]
		self.length = length

	# Forgot ord only takes a single character
	# Forgot another self.

	def HashingFunction(self, key):
		acc = 0
		for char in key:
			acc += ord(char)
		hash = acc % self.length
		return hash

	def GetKey(self, index):
		return self.__nodeArray[index].GetKey()

	def GetValue(self, index):
		return self.__nodeArray[index].GetValue()

	# Forgot self on hashing function
	# Attempted to modify key without set key

	def Insert(self, key, value):
		hash = self.HashingFunction(key)
		tableExhausted = False
		index = hash

		while self.__nodeArray[index].GetKey() != "":

			index = index + 1
			if index >= self.length:
				index = 0

			if index == hash:
				tableExhausted = True
				break

		if tableExhausted:
			print("Error - table is full.")
		else:
			self.__nodeArray[index].SetKey(key)
			self.__nodeArray[index].SetValue(value)

demarc = "-" * 58

myTable = HashTable(10)

while True:
	query = input("Enter Query:> ")
	queries = query.split(":")
	data = queries[-1].strip()
	cmd = queries[0].strip().lower()
	if cmd == "exit":
		break
	elif query.lower() == "show":
		print()
		print(demarc)
		print("|{:^10} | {:^20} | {:^20}|".format("Index", "Key", "Value"))                                                                                                                      
		print(demarc)
		for index in range(myTable.length):
			print("|{index:^10} | {id:^20} | {item:^20}|".format(index = str(index), 
				id = myTable.GetKey(index),
				item = myTable.GetValue(index)))
		print(demarc, "\n")
	elif cmd == "traverse":
		print("\n", "Start Pointer: ", myTable.GetHeadPointer())
		print("\n", demarc)
		print("|{:^10}|{:^20}|{:^10}|".format("Index", "Item", "Pointer"))
		print(demarc)
		currentPointer = myTable.GetHeadPointer()
		if currentPointer == -1:
			print("|{:^10}|{:^20}|{:^10}|".format("", "", ""))
		while currentPointer != -1:
			sleep(.2)
			print("|{index:^10}|{item:^20}|{pointer:^10}|".format(index = currentPointer, 
				item = myTable.GetItem(currentPointer), 
				pointer = myTable.GetPointer(currentPointer)))
			currentPointer = myTable.GetPointer(currentPointer)
		print(demarc, "\n")
	elif cmd == "insert":
			items = data.split(",")
			if len(items) != 2:
				print("Insert two items, a key and the value to be stored, seperated by a ','.")
			else:
				myTable.Insert(items[0], items[1])
	elif cmd == "remove" or cmd == "delete": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeDeleted = " ".join(queries)
		myTable.remove(itemToBeDeleted)
	elif cmd == "search" or cmd == "find": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeSearched = " ".join(queries)
		myTable.search(itemToBeSearched)
	else:
		print("Enter a valid command!")





	
