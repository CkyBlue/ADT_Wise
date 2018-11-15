
Screenshot gif of CLI implementation below.

The table shows data relevant to an algorithm (index values, items values, pointer values etc.)
The text below it tries to explain what is going to happen next in the algorithm. 
Each index cell has a unique color and the color is the same across index and pointer columns. 
This was intended to make it easier to follow the changes to pointers and index values.

The framework implemented breaks down a complex algorithm such as an ADT operation
like 'insert into Queue' and let's you see how the data changes as the method moves to completion.

Hopefully, it should be possible to extend the use of the framework to make any type of algorithm which controls a complex data structure easier to understand and follow along with.

Notice how the colors of the cells change as the explanation moves forward.

The command line version project requires the colorama library to work.
Run it through CLI/main.py. It uses a clear screen function which 
only seems to work when running the program on a command line so it'll be best to 
view there. The function is different for the repl.it version which is linked below.

The way I've set things up for breaking down, explaining and freezing algorithms hopwfully will also make the task
of setting up the explanation and freeze points within a function simple. Here's what the code might look like.

-----------------------
log("Explanation text") """Provides text explaining what changes are going to be made by this part of the method's algorithm through a string being passed into the log function. Eg: 'The item at index 0 should be change to Ram because blah ... blah'. The log function is passed into the function. """

log("Some more explanation text")

lock() """Freeze the function at this point and update visuals to show added explanation text and changes made to data so far, once user gives the go, unfreeze and continue"""

"""Carry out the changes described in above in program code, eg: self.dataStructure.setValue("Item", 0, "Ram")"""

lock() #The next time the method freezes, the changes made will show up, the tables will show that the item Ram has been added to index 0


-----------------------

Question 6 at "https://papers.gceguide.com/A%20Levels/Computer%20Science%20(for%20final%20examination%20in%202021)%20(9608)/9608_s15_qp_41.pdf" should give you an idea of what kind of CS questions it's supposed to be helpful for.

Run the command line version on browser: https://repl.it/@OverCky/ADT-Wise

Screenshots from the command line version on repl.it:

![Screenshot](ADTWIse.gif)
![Screenshot](Screenshot1.PNG)

The GUI version is still under work. It relies on the Kivy framework.
The framework used to freeze algorithms and control their behavior is is also being worked from scratch for the GUI.
See dummys.py for the implementation of the ADT methods and adt_wise_gui.py for how the GUI below was put together

How the GUI is coming along:

![Screenshot](GUI.gif)
