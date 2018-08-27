You can get a feel for how it is suppose to work by trying out 
'insert' on queue. The live logs for the rest aren't ready. 

Until the live logs are up, all you can do is simply run commands on ADTs
and see what the effect is on internal variables such as pointer values.

The console branch is stable (I hope), the other is not.

Run it through main.py. The console version uses a clear screen function which 
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

If you want to contribute by imparting your understanding of how certain ADT
operations are carried out, feel free to tinker with the log texts for the
console version.

Refer to adt_queue to look at how self.refresh() and self.post() are being used
for implementing the live log.
