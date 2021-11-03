# Laboration 3 
## Environment & Tools 
Window 10 pro, PyCharm 2021.2.1(Professional edition), Python 3.9.6,git version 2.33.0.windows.2 

## Purpose
The purpose of the laboration is to provide practical experience in regards to…  
- Iterative and recursive implementations!
- Working with function decoration!
- File handling!
- Usage of custom loggers!
- Separation of concerns!
- Creation of well-structured program code!  

## Procedure
To fulfill the aim of this lab I implemented pseudocode for a program that compares the computation
speed for three methods of implementation of the fibonacci series namely the iterative method, the 
recursive method and memory recursive method which stores computed values in a container and to be reused to avoid 
computing the same value multiple times. The program is run from command line and the user can provide value to be used 
as an argument. If no value is provided or the entered value is not a positive integer,30 is used as default value. 
The fibonacci values of the numbers from the given value to zero is computed using the three methods. This program has 
a function to compute the fibonacci value of a number for each of the three methods. All the functions to compute the 
fibonacci value use a measurement decorator that logs a message at INFO level when 
measurement is starting, starts a timer, computes the sequence of fibonacci values of numbers from the given value(n) 
to zero and store the values in a container while logging the sequence: value for each fifth iteration at DEBUG level, 
stop timer and calculate total time used for the computation, and return the duration and the container of values. 
The information logged at INFO and DEBUG levels is stored to a file named ass_3.log information logged at INFO level is 
printed on the console. The sequence and fibonacci values are stored to a file where the file name is the name of the 
method used with extension .txt. The files used for this project are opened in write mode to allow rewrite of file each 
time the program is run. The durations for each method is printed to the console in seconds, milliseconds, microseconds 
and nanoseconds at the end of the run. The Logger used for this project is a custom logger named "ass_3_logger" created 
and level set to DEBUG, which has file handler set to DEBUG level and a console_handler set to INFO level added to it. 



## Discussion  
 I have successfully written a working program and in the course of the lab practiced the different aspects named in 
 the aim of this project. So I believe this lab was successful. However, I am still not confident regarding report 
 writing. I got the feedback that "Procedures need to account for the work conducted, i.e. how the results were 
 produced and how problems was resolved." Does that mean I have to go into details for each of the functions I wrote in 
lab? Do I need to state in the report which parts of the program was provided and which part were my implementations? Or 
 do I need to describe how the program works stating what each part of the program does to achieve the end result?
