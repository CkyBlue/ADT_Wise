from operations import Operations
from data import DataStructure, VariableData, PointerData
from actions import Null, CallableActions, Prompts, PseudoCode
from pathfinder import resource_path

from cli import CLI_Actions, CLI_Controller

class Queue_Op(Operations):
	def __init__(self, **kwargs):
		super(Queue_Op, self).__init__(**kwargs)
		
		self.pointers = PointerData(["Head", "Tail", "Free", "Current"])
		self.data = DataStructure(["Index", "Item", "Pointer"], name = "List", size = 8)

		# PseudoCode objects
		self.pseudoCodes = {
			"insert": self.get_insert_PseudoCode(),
			"remove": self.get_remove_PseudoCode(),
			"search": self.get_search_PseudoCode()
		}

		insert = CLI_Actions(name = 'insert', 
			functionToExecute = self.insert, 
			codeObj = self.pseudoCodes["insert"],
			lockCallBack = self.lockCallBack,
			endTarget = self.endTarget)
		insert_prompt = Prompts("itemToBeInserted", "Item To Insert", self.insert_Validator_Func)
		insert.addPrompt(insert_prompt)

		self.addAction(insert)
		self.initializeData()

	def insert_Validator_Func(self, data):
		if len(str(data)) >= 20:
			return "Enter a string shorter than 20 characters."

		else:
			return True

	def insert(self, itemToBeInserted, log = Null, lock = Null, light = Null):
		"""Allows for adding an item to the tail of the queue if it is not full."""

		#Short hand
		pGet = self.pointers.getValue
		pSet = self.pointers.setValue

		dGet = self.data.getValue
		dSet = self.data.setValue

		newItem = itemToBeInserted

		light([1])
		log("We first fetch an item that we can attempt to insert into")
		log("the queue.")
		lock()

		light([2, 4])
		log("Then,")
		log("Step #1: Testing eligibility of operation.")
		log("Operation is possible only if list is not full.")
		lock()

		#@ Introduction to Free List
		log("The free nodes are chained into a list called a free list.")
		log("The 'Free_Pointer' points to the head or the beginning of this chain.")
		log("This head points to another free node which points to another free node,")
		log("and so on.")
		log("The list ends when a node points to null or -1.")
		lock()

		log("If Free_Pointer does not point to null, i.e. it's value is not -1,")
		log("the free list is not empty and thus there is at least one free node to use,")
		log("indicating that we are eligible to perform an insertion.")
		lock()

		light([2])
		log("Thus we check the value of the Free_Pointer to determine eligibility of operation.")
		log("Free_Pointer: {}".format(pGet("Free")))
		lock()

		# Check eligibility
		if pGet("Free") == -1:
			light([3])
			log("The pointer value indicating the free node to which new data can be added,")
			log("the Free_Pointer, has a null value, -1.")
			log("Thus, we know that there is no empty node to add an item to anymore")
			log("and the operation fails.")

		else:
		# Handle key operation
			light([4])
			log("Since Free_Pointer is not null, an insertion can be safely")
			log("performed on the Queue.")
			lock()

			light([5, 6])
			log("Step #2: Performing the operation of interest.")
			log("We are trying to insert an item into the queue.")
			log("Let's get that out of the way.")
			lock()

			light([5])
			log("Our item to be inserted is to be placed into the head of the free list.")
			log("Since it is the node of interest,")
			log("Current_Pointer takes the value of the Free_Pointer which is {}.".format(pGet("Free")))
			log("so that we have a way to access that particular node.")
			lock()
			pSet("Current", pGet("Free"))

			light([6])
			log("Setting item at free node to {}".format(newItem))
			lock()		
			dSet("Item", pGet("Current"), newItem)

		# Correct Flow
			light(list(range(7, 15 + 1))) # [7...15]
			log("Step #3: Correcting links for future operations.")
			log("We alter pointer values so that everything is set up such")
			log("that operations such as insertion or removal of items performed")
			log("in the future go off without a hitch")
			lock()

			log("We do this in an order that ensures that no value")
			log("is overwritten before it has gotten a chance to be used.")
			lock()

			log("There are two lists constituting the Queue,")
			log("the free list and the data list")
			log("")
			log("The data list is a chain of data items that make up the queue")
			lock()

			#@ Why the data list is set up so
			log("The way the chain is set up depends on the way data needs to behave.")
			log("The first item to be removed should point to the item which logically")
			log("comes next in the data structure.")

			log("Since a queue is a 'First In First Out' data structure,")
			log("The item at the head of the queue is the first one to be removed")
			log("when we perform a 'Remove' (also known as 'Pop') operation on a Queue.")
			lock()

			log("After we remove this item, we need to know which node is the new head of the queue.")
			log("It thus makes sense for every node to point to the node that came right after it,")
			lock()

			log("as opposed to the node that came right before it, for comparision,")
			log("which would be the case in a Stack.")
			lock()

			log("This part of the correction, however, will overwrite the pointer value of the node")
			log("at the value of Current_Pointer.")
			log("Since overwriting should come after the value has served its purpose, we deal")
			log("with the overwriting part involving the data list last.")
			log("Thus, we begin with correcting the free list.")

			# Free list
			light([7])
			log("Step #3.1: Making pointer corrections within the free list,")
			pointerTo = dGet("Pointer", pGet("Current"))
			log("The node indicated by Current_Pointer, node {},".format(pGet("Current")))
			log("itself points to index {}".format(pointerTo))
			lock()

			log("Since the node indicated by Current_Pointer was previously the")
			log("head of the free list, it points to the next logical head of the free list.")
			lock()

			if pointerTo == -1:
				log("The fact that the node indicated by the Current_Pointer points to -1")
				log("however indicates that the next head of the free pointer does not exist and")
				log("that the queue is full.")
				lock()

				log("Notice that determining if we are able to perform an insertion is")
				log("done by checking whether the free pointer is -1 (null) or not,")
				log("with -1 indicating the queue is full and")
				log("that insertion can't be performed.")
				lock()

			else:
				log("Note that as further insertions are carried out,")
				log("the nodes in the free list decrease until eventually there are none.")
				lock()

				log("By setting up the tail of the free list to have a pointer value of -1")
				log("we can use the mechanism of fetching the value of the next Free_Pointer from the")
				log("pointer value of the old free pointer to our advantage.")
				lock()

				log("An index position of -1 does not exist so ")
				log("Thus, determining if we are able to perform an insertion is")
				log("done by checking whether the free pointer is -1 (null) or not,")
				log("with -1 indicating the queue is full and")
				log("that insertion can't be performed.")
				lock()				

			log("The value of Free_Pointer changes to {}.".format(pointerTo))
			lock()
			pSet("Free", pointerTo)
			lock()

			# Data list
			light(list(range(8, 11 + 1))) # [8...11]
			log("Step #3.2: Making pointer corrections within the data list,")
			lock()
			
			log("The previous data list and the new node both need to accomodate changes.")
			lock()

			log("As mentioned earlier,")
			log("the way the chain of nodes is set up should allow for the chain to be able")
			log("to provide useful information that special pointers cannot provide")
			log("that could be useful for future operations performed on it.")
			log("")
			log("In the event a removal/pop operation is performed on the queue,")
			log("as per the nature of queues, the item at the head of the queue is removed")
			log("and the item right after becomes the newest head.")
			lock()

			log("Thus, we need to ensure that the chain allows each node to point to")
			log("the node that comes logically after it")
			log("(as opposed to the alternative of pointing to the one before).")
			lock()

			log("We achieve this by performing the relevant pointer correction operation")
			log("everytime a new node is added to the Queue.")
			lock()

			light([8, 9, 10])
			log("The previous tail of the queue (the newest addition being the Current)")
			log("is the node indicated by Tail_Pointer as we have yet to overwrite that pointer")
			log("to point to the newly added node.")
			lock()

			log("We modify the pointer of this tail node to point to the node indicated by")
			log("Current_Pointer, which is to say we store the value of Current_Pointer at the")
			log("pointer value of the mentioned tail node.")
			lock()

			light([8])
			log("We begin by checking if a previous tail exists.")
			lock()

			if pGet("Tail") != -1:
				light([9])
				log("Any value of Tail_Pointer besides -1 (which indicates a non-existent index or null)")
				log("indicates that a previous tail exists.")
				log("")
				log("The previous tail at index {} is set to point to the newest addition at {}.".format(pGet("Tail"),
					pGet("Current")))
				lock()
				dSet("Pointer", pGet("Tail"), pGet("Current"))

			else:
				log("Since Tail_Pointer has a value of -1,")
				log("we know that a tail node did not previously exist")
				log("as no node with index -1 exists and the value denotes null")
				log("so we do not need to bother with having the previous tail point to our newest addition.")
			
			light([10])
			lock()

			light([11])
			log("Since the node indicated by Current_Pointer is to be the next tail,")
			log("it does not need to point to anything.")
			lock()

			log("Thus, the pointer value of the node indicated by Current_Pointer")
			log("should have a value of -1 which represents null.")		
			lock()

			dSet("Pointer", pGet("Current"), -1)
			lock()

			light([12, 13, 14, 15])
			log("Step #3.3: Making corrections to special pointer values")
			lock()

			log("The head pointer and the tail pointer are special pointer values used")
			log("to store additional information required to allow the Queue to function")
			log("properly.")
			log("We examine how we might need to modify either.")
			lock()

			light([12])
			log("The newest node is our new tail, so")
			log("The value of Tail_Pointer is changed to that of Current_Pointer.")
			lock()

			pSet("Tail", pGet("Current"))
			lock()

			light([13, 14, 15])
			log("The Head_Pointer would only be modified in the event the newest addition")
			log("was the first addition to the Queue, in which case it would be the new head.")
			lock()

			light([13])
			log("We begin by checking whether the newest addition is the first addition")
			log("the queue.")
			lock()

			log("IF Head_Pointer has a null value, it would indicate")
			log("that no head exists as of yet, meaning the newest addition is")
			log("the logical head of the queue.")
			lock()

			if pGet("Head") == -1:
				light([14])
				log("Since Head_Pointer has a null value (-1),")
				log("we know that no previous head of the Queue exists so the")
				log("newest addition becomes a head pointer.")
				log("and Head_Pointer is set to the value of Current_Pointer, {}".format(pGet("Current")))
				lock()
				
				pSet("Head", pGet("Current"))
			
			else:
				log("Since Head_Pointer doesn't have a null value,")
				log("we know that a previous head of the Queue exists so the")
				log("modification of the Head_Pointer can be ignored.")
			lock()

			light([15, 16])
			log("All done.")
			lock()

	def get_insert_PseudoCode(self):
		f = open("queue_insert_pseudo.txt", "r")
		p = PseudoCode()
		p.extract(f.read())
		return p 

	def get_remove_PseudoCode(self):
		f = open("queue_remove_pseudo.txt", "r")
		p = PseudoCode()
		p.extract(f.read())
		return p 

	def get_search_PseudoCode(self):
		f = open("queue_search_pseudo.txt", "r")
		p = PseudoCode()
		p.extract(f.read())
		return p 

	def initializeData(self):
		#Short hand
		pGet = self.pointers.getValue
		pSet = self.pointers.setValue

		dGet = self.data.getValue
		dSet = self.data.setValue

		for i in range(self.data.size):
			dSet("Pointer", i, i + 1)
			dSet("Index", i, i)

		dSet("Pointer", self.data.size - 1, -1)

		pSet("Free", 0)
		pSet("Head", -1)
		pSet("Tail", -1)
		pSet("Current", -1)

c = CLI_Controller(source = Queue_Op)
c.loop()