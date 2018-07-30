from time import sleep

class Node:
	def __init__(self):
		self.item = ""
		self.pointer = 0

class Stack:
	def __init__(self, scope):
		self.length = scope
		self.body = [Node() for i in range(self.length)]
		self.baseOfStackPointer = -1
		self.topOfStackPointer = -1
		self.freePointer = 0
		self.initialize()

	def initialize(self):
		for index in range(self.length - 1):
			self.body[index].pointer = index + 1
		self.body[self.length - 1].pointer = -1

	def insert(self, newItem):
		if self.freePointer == -1:
			print("No free node!")
		else:
			currentPointer = self.freePointer
			self.body[currentPointer].item = newItem
			self.freePointer = self.body[currentPointer].pointer

			self.body[currentPointer].pointer = self.topOfStackPointer
			self.topOfStackPointer = currentPointer

			if currentPointer == 0:
				self.baseOfStackPointer = currentPointer

	def remove(self):
		if self.topOfStackPointer == -1:
			print("Empty Stack!")
		else:
			currentPointer = self.topOfStackPointer
			popVal = self.body[currentPointer].item
			self.body[currentPointer].item = ""

			self.topOfStackPointer = self.body[currentPointer].pointer

			self.body[currentPointer].pointer = self.freePointer
			self.freePointer = currentPointer

			if self.topOfStackPointer == -1:
				self.baseOfStackPointer = -1

			return popVal

	def search(self, itemToBeSearched):
		if self.topOfStackPointer == -1:
			print("Stack is empty!")
		else:
			currentPointer = self.topOfStackPointer
			while currentPointer != -1 and itemToBeSearched != self.body[currentPointer].item:
				currentPointer = self.body[currentPointer].pointer
			if currentPointer == -1:
				print("Item not found!")
			else:
				print("Item found at index: {}".format(currentPointer))



students = Stack(10)
demarc = "-" * 44

while True:
	query = input("Enter Query:> ")
	cmd = " ".join(query.lower().split(":")).split()[0]
	if cmd == "exit":
		break
	elif cmd ==  "show":
		print()
		print(demarc)
		print("|{:^10}|{:^20}|{:^10}|".format("Index", "Item", "Pointer"))
		print(demarc)
		for index in range(students.length):
			sleep(.2)
			print("|{index:^10}|{item:^20}|{pointer:^10}|".format(index = index, 
				item = students.body[index].item, 
				pointer = students.body[index].pointer))
		print(demarc, "\n")
		print("Base of Stack Pointer: ", students.baseOfStackPointer)
		print("Top of Stack Pointer: ", students.topOfStackPointer)
		print("Free Pointer: ", students.freePointer, "\n")
	elif cmd == "insert" or cmd == "add":
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeInserted = " ".join(queries)
		if itemToBeInserted:
			students.insert(itemToBeInserted)
	elif cmd == "remove" or cmd == "delete": 
		item = students.remove()
		if item: print(item)
	elif cmd == "search" or cmd == "find": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeSearched = " ".join(queries)
		students.search(itemToBeSearched)
	else:
		print("Enter a valid command!")
