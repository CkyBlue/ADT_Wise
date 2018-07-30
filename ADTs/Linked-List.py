from time import sleep

class Node():
	
	def __init__(self, Data, Pointer):
		self.__Data = Data # Data : string
		self.__Pointer = Pointer # Pointer : integer

	# Did not note that the method CreateNode was the constructor 
	# Did not refer to constructor specification for __init__

	def SetData(self, Data):
		self.__Data = Data

	def SetPointer(self, Pointer):
		self.__Pointer = Pointer

	def GetData(self):
		return self.__Data

	def GetPointer(self):
		return self.__Pointer

class LinkedList():

	def __init__(self):
		
		self.__HeadPointer = -1 # HeadPointer : Integer
		self.__FreeListPointer = 0 # FreeListPointer : Integer
		self.__NodeArray = [Node("", i + 1) for i in range(10)] ## Alternatively [..] * 10
		self.__NodeArray[9].SetPointer(-1)

		self.length = 10

	# Forgot that ADT is initialized with the free list already linked

	def GetHeadPointer(self):
		return self.__HeadPointer

	def GetFreePointer(self):
		return self.__FreeListPointer

	# Returned GetData instead of GetData()

	def GetItem(self, Pointer):
		return self.__NodeArray[Pointer].GetData()

	def GetPointer(self, Pointer):
		return self.__NodeArray[Pointer].GetPointer()

	def InsertItem(self, ItemToBeInserted):

		if self.__FreeListPointer == -1:	# Eligibility Check
			
			print("Error - list is full.")

		else:
			
			newNodePointer = self.__FreeListPointer 
			self.__NodeArray[newNodePointer].SetData(ItemToBeInserted) # Operation Of Interest
			self.__FreeListPointer = self.__NodeArray[newNodePointer].GetPointer() # Free List

			# Forgot to do flow correction for free list
			# In insertion, free list must be handled before data list, against premature overwrite
			# The special pointer handling is in contrast to use of previousNodePointer only
			# Mistakenly put all flow control in the contrast, no flow control

			nextNodePointer = self.__HeadPointer
			while nextNodePointer != -1 and self.__NodeArray[nextNodePointer].GetData() < ItemToBeInserted: # Traversal

				previousNodePointer = nextNodePointer
				nextNodePointer = self.__NodeArray[previousNodePointer].GetPointer()

			if nextNodePointer == self.__HeadPointer: # Flow Correction
				
				self.__HeadPointer = newNodePointer # Special Pointers
			else:

				# Performed a str + int operation inside print()

				self.__NodeArray[previousNodePointer].SetPointer(newNodePointer) # Data List

			self.__NodeArray[newNodePointer].SetPointer(nextNodePointer)

	# When handling -1 as flow control, make sure it's not loaded into an index

	def FindItem(self, searchItem):

		thisNode = self.__HeadPointer

		while thisNode != -1 and self.__NodeArray[thisNode].GetData() < itemToBeSearched: # Dead end and logical end

			thisNode = self.__NodeArray[thisNode].GetPointer()

		if thisNode != -1 and self.__NodeArray[thisNode].GetData() == itemToBeSearched:
			return thisNode
		else:
			return -1

# Made a mistake here, list empty if current Pointer = head Pointer, not only current Pointer = -1, 2nd can mean hitting the end of the list   
# Another mistake, actualy no, same mistake , head Pointer = -1 means empty list, cP = hP can mean record found in hP
# Forgot to change the data itself (granted in reality, you probably woundn't erase the data yet)

	def DeleteItem(self, item):
		
		currentPointer = self.__HeadPointer

		while currentPointer != -1 and self.__NodeArray[currentPointer].GetData() < item: # Traverse

			previousNodePointer = currentPointer
			currentPointer = self.__NodeArray[currentPointer].GetPointer()


		if self.__NodeArray[currentPointer].GetData() != item: # Eligibility check
			if self.__HeadPointer == -1:
				print("List is empty.")
			else:
				print("Entry not found")
		else:
	
			nextPointer = self.__NodeArray[currentPointer].GetPointer()
			if self.__HeadPointer == currentPointer:
				self.__HeadPointer =  nextPointer # Special Pointers

			else:
				self.__NodeArray[previousNodePointer].SetPointer(nextPointer) # Data list ->.

			self.__NodeArray[currentPointer].SetData("")

			self.__NodeArray[currentPointer].SetPointer(self.__FreeListPointer) # Free list .->
			self.__FreeListPointer = currentPointer 

demarc = "-" * 44

students = LinkedList()

while True:
	query = input("Enter Query:> ")
	cmd = " ".join(query.lower().split(":")).split()[0]
	if cmd == "exit":
		break
	elif cmd ==  "show":
		print("\n", demarc)
		print("|{:^10}|{:^20}|{:^10}|".format("Index", "Item", "Pointer"))
		print(demarc)
		for index in range(students.length):
			sleep(.2)
			print("|{index:^10}|{item:^20}|{pointer:^10}|".format(index = index, 
				item = students.GetItem(index), 
				pointer = int(students.GetPointer(index))))
		print(demarc, "\n")
		print("Start Pointer: ", students.GetHeadPointer())
		print("Free Pointer: ", students.GetFreePointer(), "\n")
	elif cmd == "traverse":
		print("\n", "Start Pointer: ", students.GetHeadPointer())
		print("\n", demarc)
		print("|{:^10}|{:^20}|{:^10}|".format("Index", "Item", "Pointer"))
		print(demarc)
		currentPointer = students.GetHeadPointer()
		if currentPointer == -1:
			print("|{:^10}|{:^20}|{:^10}|".format("", "", ""))
		while currentPointer != -1:
			sleep(.2)
			print("|{index:^10}|{item:^20}|{pointer:^10}|".format(index = currentPointer, 
				item = students.GetItem(currentPointer), 
				pointer = students.GetPointer(currentPointer)))
			currentPointer = students.GetPointer(currentPointer)
		print(demarc, "\n")
	elif cmd == "insert" or cmd == "add":
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeInserted = " ".join(queries)
		if itemToBeInserted:
			students.InsertItem(itemToBeInserted)
	elif cmd == "remove" or cmd == "delete": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeDeleted = " ".join(queries)
		students.DeleteItem(itemToBeDeleted)
	elif cmd == "search" or cmd == "find": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeSearched = " ".join(queries)
		print(students.FindItem(itemToBeSearched))
	else:
		print("Enter a valid command!")