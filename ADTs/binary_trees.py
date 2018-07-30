from time import sleep

class Node:
	def __init__(self):
		self.item = ""
		self.leftPointer = 0
		self.rightPointer = 0

class BinaryTree:
	def __init__(self, scope):
		self.length = scope
		self.body = [Node() for i in range(self.length)]
		self.rootPointer = -1
		self.freePointer = 0
		self.initialize()

	def initialize(self):
		for index in range(self.length):
			self.body[index].leftPointer = index + 1
			self.body[index].rightPointer = -1
			self.body[index].item = ""
		self.body[self.length - 1].leftPointer = -1

	def insert(self, itemToBeInserted):
		if self.freePointer == -1:
			print("Tree is full!")
		else:
			currentPointer = self.freePointer
			self.freePointer = self.body[currentPointer].leftPointer

			self.body[currentPointer].item = itemToBeInserted
			self.body[currentPointer].leftPointer = -1
			self.body[currentPointer].rightPointer = -1

			thisPointer = self.rootPointer
			while thisPointer != -1:
				prevPointer = thisPointer
				if self.body[thisPointer].item > itemToBeInserted:
					turnedLeft = True
					thisPointer = self.body[thisPointer].leftPointer
				else:
					turnedLeft = False
					thisPointer = self.body[thisPointer].rightPointer	 
			if thisPointer == self.rootPointer:
				self.rootPointer = currentPointer
			else:
				if turnedLeft:
					self.body[prevPointer].leftPointer = currentPointer
				else:
					self.body[prevPointer].rightPointer = currentPointer

	def traverseTree(self, root):
		if self.body[root].leftPointer != -1:
			self.traverseTree(self.body[root].leftPointer)
		self.accumulator.append({"index" : root, 
			"left" : self.body[root].leftPointer,
			"right" : self.body[root].rightPointer,
			"item" : self.body[root].item})
		if self.body[root].rightPointer != -1:
			self.traverseTree(self.body[root].rightPointer)


	def traverse(self):
		self.accumulator = []
		if self.rootPointer != -1:
			self.traverseTree(self.rootPointer)
		return self.accumulator[:]

students = BinaryTree(10)
demarc = "-" * 65

while True:
	query = input("Enter Query:> ")
	cmd = " ".join(query.lower().split(":")).split()[0]
	if cmd == "exit":
		break
	elif cmd ==  "show":
		print()
		print(demarc)
		print("|{:^10}|{:^15}|{:^20}|{:^15}|".format("Index", "Left Pointer", "Item", "Right Pointer"))
		print(demarc)
		for index in range(students.length):
			sleep(.2)
			print("|{index:^10}|{leftPointer:^15}|{item:^20}|{rightPointer:^15}|".format(index = index, 
				item = students.body[index].item, 
				leftPointer = students.body[index].leftPointer,
				rightPointer = students.body[index].rightPointer))
		print(demarc, "\n")
		print("Root Pointer: ", students.rootPointer)
		print("Free Pointer: ", students.freePointer, "\n")
	elif cmd == "traverse":
		data = students.traverse()
		if data:
			print()
			print(demarc)
			print("|{:^10}|{:^15}|{:^20}|{:^15}|".format("Index", "Left Pointer", "Item", "Right Pointer"))
			print(demarc)
			for node in data:
				sleep(.2)
				print("|{index:^10}|{leftPointer:^15}|{item:^20}|{rightPointer:^15}|".format(index = node["index"], 
				item = node["item"], 
				leftPointer = node["left"],
				rightPointer = node["right"]))
		print(demarc, "\n")
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
