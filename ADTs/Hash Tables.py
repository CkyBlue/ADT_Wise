from time import sleep

class Node():
	def __init__(self):
		self.__Key = 0 # Key : Integer
		self.__Data = "" # Data : String

	def setKey(self, key):
		self.__Key = key 

	def setData(self, data):
		self.__Data = data

	def getKey(self):
		return self.__Key

	def getData(self):
		return self.__Data

length = 10

# Forgot to consider tracker and flag, entering the loop 

class HashTable():
	def __init__(self, length):
		self.__NodeArray = [Node() for i in range(length)] # NodeArray : List
		self.__Length = length # Length : Integer

	def Hash(self, key):
		try:
			return int(key) % self.__Length
		except:
			return -1

	def getKey(self, index):
		return self.__NodeArray[index].getKey()

	def getData(self, index):
		return self.__NodeArray[index].getData()

	def InsertItem(self, id, item):
		
		try:
			id = int(id)
		except:
			print("Id is not valid. Insertion failed.")
			return None

		homeLocation = self.Hash(id)

		pointer = homeLocation
		tableExhausted = False
		while self.__NodeArray[pointer].getKey() != 0 and not tableExhausted: # Traverse

			pointer += 1

			if pointer >= self.__Length:
				pointer = 0

			if pointer == homeLocation:
				tableExhausted = True

		if not tableExhausted: # Eligibility check

			self.__NodeArray[pointer].setKey(id)
			self.__NodeArray[pointer].setData(item)

		else: 
			print("Table is full. Insertion failed.")

myTable = HashTable(length)
myTable.InsertItem(12, "Aayam")
myTable.InsertItem(22, "Kabita")
myTable.InsertItem(46, "Hari")

demarc = "-" * 58

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
		for index in range(10):
			print("|{index:^10} | {id:^20} | {item:^20}|".format(index = str(index), 
				id = myTable.getKey(index),
				item = myTable.getData(index)))
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
