# Project
## Environment & Tools 
Window 10 pro, PyCharm 2021.2.1(Professional edition), Python 3.9.6,git version 2.33.0.windows.2 

## Purpose
The purpose of this project assignment is to demonstrate the understanding of the learning objectives 
of the course covered in the course's various modules.   

## Procedure
To fulfill the purpose of this project, I have written a program for a cellular automation known as The 
Game of Life(Gol) conceived by the mathematician John Conway in 1970 to provide an elegant representation for how 
simple life can evolve. The world of Game is made up of an infinite, two-dimensional orthogonal grid of square cells, 
each of which is in one of two possible states, live or dead. Each cell interacts with the eight neighbouring cells, 
which are directly adjacent in horizontal, vertical and diagonal directions. The simulation progresses through steps 
in time with each step representing a new generation. The simulation starts with an initial cell pattern known as 
the seed of the system. The seed forms the first generation and as the simulation progresses, each new generation 
is a function of the previous generation. The state of each cell for the next generation is determined by the state 
of it's eight neighbours in the current generation following the rules below.   
 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
 2. Any live cell with two or three live neighbours lives on to the next generation.
 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. 
 5. Any live cell that survive more than 5 consecutive generations becomes and elder
 6. Any elder still alive by the 11th successive generation becomes a prime elder

The general design for this project together with some inherent code for certain functionality was provided which 
include constant declarations for the different cell states and methods to format output value for printing, update 
progress information in console, clear the console, get predefined pattern for the initial seed and the main program 
execution. The task of this project is to complete the program by writing code for certain functionalities. Below is a 
description of how this program works and the implementations I carried ou to complete to fulfill the purpose of this 
project.  
This program is run using command line and to start the program, the user can either provide the desired world size, 
number of generations to be generated, and the seed pattern to be used as an argument in the command, or the user can 
enter the name of a json file from which the world information can be read from.   
When the world information is passed with as and argument, entered the world size should be two integers seperated 
by an 'x'. I wrote a function that parse and validates the world size, by splitting the entered data at 'x', checking 
if the split results to exactly two elements, if the elements are whole numbers greater than zero. If all 
these conditions are fulfilled, then the entered size is returned as two integers corresponding to the width and height 
of the world and will be used for the simulation. However, if the world size is invalid, an appropriate error message 
is printed in the console for the user and a default world size "80x40" is used. The seed pattern name entered by the 
user is used in to populate the world with the initial seed cell population. Gliders, pulsar and penta are predefined 
seed patterns that can be used in this simulation. I wrote a function to populate the world which makes use of the 
entered pattern name and the parsed world size. For each position in the world, if the position is found on the first 
or last row or first or last column then the cell state is said to be a rim cell and the state is set to STATE_RIM. 
If the cell is not a rim cell then state of the cell depends on the users pattern choice. The pattern and world size 
is passed to a function provided with project that returns a list of positions to hold live cells if the pattern is one 
of the predefined seed patterns, otherwise it returns none. If the pattern is one of the predefined patterns, the cell 
state is determined by checking If the position is found in the returned pattern list in which case the cell should be 
alive and the state set to STATE_ALIVE otherwise the cell should be dead and state set to STATE_DEAD. However, if no 
pattern choice was entered, i.e pattern is None or the user's choice does not match any of the predefined patterns, 
cells are determined same as above, but cell state for each non-rim position is determined by randomization whereby a 
random int in the range 0 to 20 is gotten and if the integer is greater than 16, the cell should be alive otherwise the 
cell should be dead. The world is stored as a dictionary whereby each position is mapped to cell details or to None if 
the coordinate is to a rim cell. The cell detail of each cell is also stored as a dictionary in which the cell state is 
mapped to a list of the cell's neighbours and the key 'age' holds a counter for how many consecutive generation the cell 
survives which is initialized to zero.   
When the population is being read from the file, all information about the world except the age attribute is provided. 
I wrote a function that reads data from the file. This function receives the file name and adds the .json extension if 
absent, opens and reads the file, check that the data parts is of expected types, and if all is as expected then the 
information is extracted, parsed where required and stored in a new dictionary the right world format to be used in the 
program and returned. If file read fails or data is not of expected types, an appropriate error message is printed in 
the console with the help of exception handling and the program ends. The data is read from file is stored as a 
dictionary and all the keys which correspond to the coordinates are stored as string and are therefore converted to 
tuple which is the correct format required for this program. Also, each neighbour in the neighbour list comes as a list 
and is converted to a tuple for consistency even though the operations to be carried on the tuple would work just fine 
with list. An age attribute is also added and the counter initialized to zero. All the parsed data is stored as a 
dictionary in the same format as mentioned above for populating sells and the dictionary and world size are returned.   
Once the world is generated with the initial seed population, the simulation can start running. To run the simulation I 
have written a function that runs the simulation which receives a current generation, world size and number of generations the 
simulation should run. This function encapsulates another function that update world and represents a single tick of the 
simulation. The run simulation uses a decorator to loop through the generations and log information from the run. 
The function I have written to update world receives the current population and world size as arguments, prints the 
state of all the cells in the current world, determine the cell states and age of each cell for the next generation, 
then store and return a copy of the world with the updated states and age in a new dictionary which becomes the current 
cell for the next generation. The states of the cells is determined by checking the state of the neighbouring cells and 
counting the number of neighbours that are alive, then applying the rules stated above for determining state for next 
generation. Live cells include alive cells, elders and prime elders. If cell lives on to next generation, the age 
counter is increased by 1. In the decorator used to by the function that runs the simulation, the number of ordinary 
cells non-rim cells are counted just once before looping through the generations since it is the same for all generations 
while the number of life cells, dead cells, elders and prime cells are counted for each generation and this information 
is logged for each generation to a file as the simulation progresses. For each generation the run simulation function 
is called which in turn calls the update world function that prints current population on the screen and returns the new 
generation which the decorator stores and uses as the current generation to call the run simulation function for the next loop. 
The simulation is delayed for 200milliseconds before next generation is run. I created the logger used such that logger 
named 'gol_logger' opens a file named gol.log in write mode in the directory resources found in the folder containing 
project folder. The logger logs data to file at INFO level.

 
## Discussion  
This project definitely covered all sections of this course. I attempted up to the Grade A level. It was very interesting 
and challenging. My greatest challenge was arranging my code such that it could be clear and readable. I achieved this 
by splitting the code to sub-functions using both inner functions and stand_alone functions. For example in  populate_world 
function, I used the inner function inorder to still  have direct access to some the outer function's local variable. In 
the case of the function load_seed_from_file where sub functions were many and long I wrote stand-alone functions to avoid 
overcrowding and too long functions. For code that I used more than once I also wrote a function to avoid repetition like 
in the case of the is_rim_cell and get_state_from_cell_detail function. The other challenge I had was figuring out the 
format of the coordinates. Since coordinates are mostly represented in the x,y format it took a while to realize that the 
coordinates obtained from get_pattern was reversed. I decided to use the same format for the whole program for consistency. 
For the function to read from file, the challenge was the fact that world had so many sets of data with nested 
dictionary and list. It helped a lot with the validation and parsing when I the different parts to separate functions 
returned the different components already stored in its container instead of trying to handle all the different parts in 
one function which would have required to be nested code in multiple levels.
For the implementation for Grade A, there was a tip that file does not have an age attribute, and it is most appropriate 
to compensate for it in world update. I thought of checking if current generation has age attribute and if not then it 
is added. But this will mean that this check will have to be done for every generation which is unnecessary, I felt it 
was best to add the key attribute when world is populated and when file is read, and base of the current knowledge I 
could not think of a reason why this will not be appropriate. The next challenge was getting the 
state of cell from world. Since the value of state vary from cell to cell and generation to generation, it became more
complicated to get the state after age attribute is added and state is not the only key. I solved this by getting all 
keeps and since there are only two keys, assign the key that is not 'age' to state. I wonder if there is a better 
approach. When it comes to the report writing, I am still not confident about what needs to be included or not even after 
feedback from previous lab. I have tried to give more details of on how I reasoned for the functions i had to write while 
I describe how the program works. I hope this approach meet the requirements. 
Overall, I think the project required a lot of logical reasoning and design apart from knowledge of available 
tools we learned from the different sections. It was a very interesting project to work with and the course material 
was enough to provide the skills requirement to carry out this project.