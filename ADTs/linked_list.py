from time import sleep

class Node:
	def __init__(self):
		self.item = ""
		self.pointer = 0

class LinkedList:
	def __init__(self, scope):
		self.length = scope
		self.body = [Node() for i in range(self.length)]
		self.initialize()
		self.startPointer = -1
		self.freePointer = 0

	def initialize(self):
		for index in range(self.length - 1):
			self.body[index].pointer = index + 1
		self.body[self.length - 1].pointer = -1

	def insert(self, newItem):
		if self.freePointer == -1:
			print("No free nodes!")
		else:
			currentPointer = self.freePointer
			self.body[currentPointer].item = newItem
			self.freePointer = self.body[currentPointer].pointer

			thisPointer = self.startPointer
			if thisPointer != 1 and self.body[thisPointer].item < newItem:
				prevPointer = thisPointer
				thisPointer = self.body[thisPointer].pointer
			if thisPointer == self.startPointer:
				self.startPointer = currentPointer
			else:
				self.body[prevPointer].pointer = currentPointer
			self.body[currentPointer].pointer = thisPointer

	def remove(self, itemToBeDeleted):
		if self.startPointer == -1:
			print("The list is empty!")
		else:
			currentPointer = self.startPointer
			while currentPointer != -1 and self.body[currentPointer].item != itemToBeDeleted:
				prevPointer = currentPointer
				currentPointer = self.body[currentPointer].pointer
			if currentPointer != -1:
				if self.startPointer == currentPointer:
					self.startPointer = self.body[currentPointer].pointer
				else:
					self.body[prevPointer].pointer =  self.body[currentPointer].pointer
				self.body[currentPointer].pointer = self.freePointer
				self.freePointer = currentPointer
				self.body[currentPointer].item = ""
			else:
				print("Item not found!")

	def search(self, itemToBeSearched):
		if self.startPointer == -1:
			print("List is empty!")
		else:
			currentPointer = self.startPointer
			exhausted = False
			while not exhausted and itemToBeSearched != self.body[currentPointer].item:
				currentPointer = self.body[currentPointer].pointer
				if itemToBeSearched < self.body[currentPointer].item or currentPointer == -1:
					exhausted = True
			if not exhausted:
				print("Item found at index: {}.".format(currentPointer))
			else:
				print("Item not found!")

students = LinkedList(10)
demarc = "-" * 44

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
				item = students.body[index].item, 
				pointer = students.body[index].pointer))
		print(demarc, "\n")
		print("Start Pointer: ", students.startPointer)
		print("free Pointer: ", students.freePointer, "\n")
	elif cmd == "traverse":
		print("\n", "Start Pointer: ", students.startPointer)
		print("\n", demarc)
		print("|{:^10}|{:^20}|{:^10}|".format("Index", "Item", "Pointer"))
		print(demarc)
		currentPointer = students.startPointer
		if currentPointer == -1:
			print("|{:^10}|{:^20}|{:^10}|".format("", "", ""))
		while currentPointer != -1:
			sleep(.2)
			print("|{index:^10}|{item:^20}|{pointer:^10}|".format(index = currentPointer, 
				item = students.body[currentPointer].item, 
				pointer = students.body[currentPointer].pointer))
			currentPointer = students.body[currentPointer].pointer
		print(demarc, "\n")
	elif cmd == "insert" or cmd == "add":
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeInserted = " ".join(queries)
		if itemToBeInserted:
			students.insert(itemToBeInserted)
	elif cmd == "remove" or cmd == "delete": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeDeleted = " ".join(queries)
		students.remove(itemToBeDeleted)
	elif cmd == "search" or cmd == "find": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeSearched = " ".join(queries)
		students.search(itemToBeSearched)
	else:
		print("Enter a valid command!")
## Check subscript
## Decompose references to raw sources to ascertain behaviour