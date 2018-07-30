from time import sleep

BinaryTree = [[0, "", 0] for i in range(10)]

def initializeTree(Tree):

	# Left Pointers linked into free list

	for i in range(len(Tree)):
		Tree[i][0] = i + 1
		Tree[i][2] = -1

	Tree[len(Tree) - 1][0] = -1

initializeTree(BinaryTree)

freePointer = 0
rootPointer = -1

# freePointer and rootPointer hadn't been defined to behanve as global
# forgot to handle the data itself in op of interest

def Insert(data):

	global freePointer
	global rootPointer

	if freePointer == -1: # Eligibility check
		print("Tree is full.")

	else:
		newNodePointer = freePointer # Op of Interest
		freePointer = BinaryTree[newNodePointer][0] # Free list
		BinaryTree[newNodePointer][1] = data # Data list .

		nextPointer = rootPointer # Traversal
		while nextPointer != -1:

			previousPointer = nextPointer

			if data < BinaryTree[nextPointer][1]:
				nextPointer = BinaryTree[nextPointer][0]
				turned_left = True
			else:
				nextPointer = BinaryTree[nextPointer][2]
				turned_left = False
			
		if nextPointer == rootPointer:
			rootPointer = newNodePointer # Special Pointers

		# Plugged in wrong pointer value into previous pointers

		else:
			if turned_left: # Data list ->.
				BinaryTree[previousPointer][0] = newNodePointer
			else:
				BinaryTree[previousPointer][2] = newNodePointer

		BinaryTree[newNodePointer][0] = -1 # Data list .->

def Traverse(root):

	if BinaryTree[root][0] != -1:
		Traverse(BinaryTree[root][0])
	
	print(BinaryTree[root][1])
	
	if BinaryTree[root][2] != -1:
		Traverse(BinaryTree[root][2])

demarc = "-" * 71

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
		print("|{:^10} | {:^15} | {:^20} | {:^15}|".format("Index", "Left Pointer", "Data", "Right Pointer"))                                                                                                                      
		print(demarc)
		for index in range(len(BinaryTree)):
			print("|{index:^10} | {left:^15} | {data:^20} | {right:^15}|".format(index = str(index), 
				left = BinaryTree[index][0],
				right = BinaryTree[index][2],
				data = BinaryTree[index][1]))
		print(demarc, "\n")
		print("Free Pointer: ", freePointer)
		print("Root Pointer: ", rootPointer)
		print("\n")
	elif cmd == "traverse":
		print(Traverse(rootPointer))
	elif cmd == "insert":
			items = data
			if items == "":
				print("Insert ... what?")
			else:
				Insert(items)
	elif cmd == "search" or cmd == "find": 
		queries = " ".join(query.split(":")).split()[1:]
		itemToBeSearched = " ".join(queries)
		myTable.search(itemToBeSearched)
	else:
		print("Enter a valid command!")
