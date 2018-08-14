The project is basically a polished integration of programs I'd made during 
my A2 year to help me practise ADTs. 

Until the live logs are up, all you can do is simply run commands on ADTs
and see what the effect is on internal variables such as pointer values.

The live logs are supposed to explain the steps involved in each action in more
depth but they still need more work.

I hoped that this program to be helpful to those that might be struggling
with ADTs. I'd found it a tough concept to really get comfortable with myself.
I'm not yet convinved of the utility of this endeavor but its pulling along just fine
so far.

So far I've adapted hash-table, queue, stack and linked-list.

You can get a feel for how it is suppose to work by trying out 
'insert' on queue. The live logs for the rest aren't ready. 

Run it through main.py. The program uses a clear screen function which 
only works when running the program on a terminal so it'll be easiest to 
view the program on terminal.

I hope to get the rest adapted in time. The ones adapted are open to being 
refined. 

Adapted:
	Queue
	Hash-Table
	Stack
	Linked-list

Real-time log:
	Queue: 66% done
	Hash-Table: 0% done
	Stack: 0% done
	Linked-list: 0% done
	
---------------------------------------
It looks like bringing the project to a GUI will mean adts are going to
have to implemented somewhat differently. For the time being, I think I
will have the GUI version and the console version on seperate branches.

If you want to contribute by imparting your understanding of how certain ADT
operations are carried out, feel free to tinker with the log texts for the
console version.

Refer to adt_queue to look at how self.refresh() and self.post() are being used
for implementing the live log.
