x = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o']

for index in range(1, len(x)):
	itemToBeInserted = x[index]
	currentItemPointer = index - 1
	while (x[currentItemPointer] > itemToBeInserted) and currentItemPointer >= 0:
		x[currentItemPointer + 1] = x[currentItemPointer]
		currentItemPointer -= 1
	x[currentItemPointer + 1] = itemToBeInserted
	print(x)

print(" ", x)
