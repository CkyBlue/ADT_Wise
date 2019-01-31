from operations import Operations
from data import DataStructure, VariableData, PointerData
from actions import Null, CallableActions, Prompts, PseudoCode
from pathfinder import resource_path

class Queue_Op(Operations):
	def __init__(self, **kwargs):
		super(Queue_Op, self).__init__(**kwargs)
		
		self.variables = VariableData(["A", "B", "C", "Limit"])

		# PseudoCode objects
		self.pseudoCodes = {
			"fibonacci": self.get_fibonacci_PseudoCode()
		}

		self.addAction(
			CLI_Actions(name = 'Generate fibonacci sequence', 
			functionToExecute = self.seq_fibonacci, 
			codeObj = self.pseudoCodes["fibonacci"],
			lockCallBack = self.lockCallBack,
			endTarget = self.endTarget)
			)
		# self.initializeData()

	def seq_fibonacci(self, log = Null, lock = Null, light = Null):
		"""Outputs the first 10 items in the Fibonacci sequence"""

		#Short-hand
		vGet = self.variables.getValue
		vSet = self.variables.setValue

		light([0])
		log("We will be looking at an algorithm which generates")
		log("a sequence of numbers - the fibonacci sequence.")
		log("")
		log("We will stop at the 10th item in the sequence.")
		lock()

		log("To summarize the fibonacci sequence,")
		log("each term, except for the first two defined as 0 and 1,")
		log("is the sum of the two items before it.")
		lock()

		log("For e.g, the 23rd item is the sum of the 21st and 22nd,")
		lock()

		light([1, 2])
		log("We know, for starters, that the first two items are 0 and 1")
		log("so, let's start by telling our program that through two variables")
		log("we call A and B here.")
		lock()

		vSet("A", 0)
		vSet("B", 1)

		light([3])
		log("Since we are only interested in 10 items, we tell our program that as well")
		log("through a variable we call Limit here.")
		lock()
		vSet("Limit", 10)

		light([5])
		log("Since we need to repeatedly calculate sums to generate new terms,")
		log("we can expect the need for iterations in our program.")
		lock()

		log("If we were to generate one new term of the sequence")
		log("with each iteration, we would need to iterate from the 3rd term")
		log("onward, not the 1st, till the 10th since producing the first two terms")
		log("0 and 1 does not involve the same computation that producing the rest does.")
		lock()

		light([4])
		log("Thus we can output the first two terms in the sequence")
		log("even before we head into the iteration.")
		lock()

		arr = ["0", "1"]
		log("OUTPUT:")
		log(" ".join(arr))
		lock()

		light([5])
		log("Notice we iterate (Limit - 2) times")
		log("since there are (Limit - 2) terms between Limit and 3.")
		lock()

		log("in our current case,")
		log("there are 8 terms between the 10th term and the 3rd.")
		lock()

		for i in range(vGet("Limit") - 2):
			light([6])
			log("Consider the way we generate a new term for each iteration,")
			log("Term {} is the sum of term {} and term {}".format(i + 3, i + 1, i + 2))
			lock()

			log("Term {} is stored in A, and term {} in B".format(i + 1, i + 2))
			log("So the next term in the fibonacci sequence is the sum of A and B.")
			log("which we store in the variable we named C")
			lock()

			vSet("C", vGet("A") + vGet("B"))
			log("Thus C = A + B = {}".format(vGet("C")))
			lock()
			
			light([7])
			arr.append(str(vGet("C")))
			log("OUTPUT:")
			log(" ".join(arr))
			lock()

			light([8, 9])
			log("Now, we need to ensure that the next iteration,")
			log("if there is one, produces the correct next term as well.")
			lock()

			log("For the next term, term {}".format(i + 4))
			log("We need to have term {} as A and term {} as B".format(i + 2, i + 3))
			log("if we are to get the correct C = A + B for the next iteration")
			log("where C will give term {}".format(i + 4))
			lock()

			vSet("A", vGet("B"))
			vSet("B", vGet("C"))
			lock()

		log("No more iterations.")
		log("OUTPUT:")
		log(" ".join(arr))
		lock()

	def get_fibonacci_PseudoCode(self):
		f = open("fibonacci_pseudo.txt", "r")
		p = PseudoCode()
		p.extract(f.read())
		return p 
