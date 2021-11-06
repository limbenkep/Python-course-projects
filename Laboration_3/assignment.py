#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 3
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - create_logger()
 - measurements_decorator(..)
 - fibonacci_memory(..)
 - print_statistics(..)
 - write_to_file(..)
"""
import sys
from pathlib import Path
from timeit import default_timer as timer
from functools import wraps
import argparse
import logging
import logging.config
import json

__version__ = '1.1'
__desc__ = "Program used for measuríng execution time of various Fibonacci implementations!"

RESOURCES = Path(__file__).parent / "../_Resources/"


def create_logger() -> logging.Logger:
    """Create and return custom logger object."""

    #logger can also be created by reading from file (teacher's feedback)
    #with open(RESOURCES / "ass3_log_conf.json") as file:
        #logging.config.dictConfig(json.load(file))
        #return logging.getLogger('ass_3_logger')


    #Create logger named ass_3_logger and set to DEBUG level
    logger = logging.getLogger("ass_3_logger")
    logger.setLevel(logging.DEBUG)

    # Create console handler and set to INFO level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create file handler that log to file 'ass_3.log opened in write more and set to DEBUG level
    log_path = RESOURCES / "ass_3.log"
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setLevel(logging.DEBUG)

    #Set logging formatting style for handlers
    console_format = logging.Formatter("%(levelname)s | %(message)s")
    file_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def measurements_decorator(func):
    """Function decorator, used for time measurements."""
    #wrapper gets the number nth_nmb from the func parameter list
    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:
        result = list()
        #get time at which measurement starts
        start_time = timer()
        #log a message to logger at INFO level at the beginning of the measurement,
        LOGGER.info("Starting measurements...{}".format(func.__name__))
        counter = 0
        #loops through numbers from the nth_nmb to zero
        for nth_nmb in range(nth_nmb, -1, -1):
            #run func for each of the numbers and store the result in a list
            result.append(func(nth_nmb))
            #check if number of iteration is divisible by 5. if yes logg number and value at DEBUG level
            if counter % 5 == 0:
                LOGGER.debug("{}: {}".format(nth_nmb, result[counter]))
            counter += 1
        #Compute duration by subtracting start time form current time
        duration = timer() - start_time
        #return the time taken for the computation and the list of results as a tuple
        return duration, result
    return wrapper


"""Better approach from feedback
def measurements_decorator(func):
  #Function decorator, used for time measurements.
  @wraps(func)
  def wrapper(nth_nmb: int) -> tuple:
    values = list()
    start = timer()
    LOGGER.info("Starting measurements...{}".format(func.__name__))
    for counter, nmb in enumerate(range(nth_nmb, -1, -1)):
      value = func(nmb)
      if counter % 5 == 0:
        LOGGER.debug("{}: {}".format(nmb, value))
      values.append(value)
    duration = timer() - start
    return duration, values
  return wrapper"""


@measurements_decorator
def fibonacci_iterative(nth_nmb: int) -> int:
    """An iterative approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    old, new = 0, 1
    if nth_nmb in (0, 1):
        return nth_nmb
    for __ in range(nth_nmb - 1):
        old, new = new, old + new
    return new


@measurements_decorator
def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""

    def fib(_n):
        return _n if _n <= 1 else fib(_n - 1) + fib(_n - 2)

    return fib(nth_nmb)


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """Computes Fibonacci value using recursive method. """
    #Dictionary storing all number and computed fib value
    memory = {0: 0, 1: 1}

    def fib_memory(n):
        #check if n is not found in memory
        if n not in memory:
            #the length of memory is equal to the last stored number + 1,
            # which is the next number to be computed
            n_index = len(memory)
            #compute fib value of the next value by adding the last 2 fib values in memory
            memory[n_index] = memory[n_index - 1] + memory[n_index - 2]
            #This line will keep calling recursively untill fib value of n is found in memory
            fib_memory(n)
        return memory[n]

    return fib_memory(nth_nmb)


def duration_format(duration: float, precision: str) -> str:
    """Function to convert number into string. Switcher is dictionary type here.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    switcher = {
        'Seconds': "{:.5f}".format(duration),
        'Milliseconds': "{:.5f}".format(duration * 1_000),
        'Microseconds': "{:.1f}".format(duration * 1_000_000),
        'Nanoseconds': "{:d}".format(int(duration * 1_000_000_000))
    }

    # get() method of dictionary data type returns value of passed argument if it is present in
    # dictionary otherwise second argument will be assigned as default value of passed argument
    return switcher.get(precision, "nothing")


def print_statistics(fib_details: dict, nth_value: int):
    """Function which handles printing to console."""
    line = '\n' + ("---------------" * 5)
    print_title = "DURATION FOR EACH APPROACH WITHIN INTERVAL: " + str(nth_value) + "-0"
    #collection of heading to be used for the printout
    precisions = ("Seconds", "Milliseconds", "Microseconds", "Nanoseconds")
    #Get column with for print out by add 2 to the length of the longest column heading
    col_width = max(len(word) for word in precisions) + 2
    #print headings with the above coloun with with the first column having no heading and
    #for each heading in precision
    print("{:<{width}} {:>{width}} {:>{width}} {:>{width}} {:>{width}}".
          format("", *precisions, width=col_width))
    #For each method pint duration of measurement in seconds, millisecond, microseconds, nanoseconds
    for fib_type, details in fib_details.items():
        row = "{:<{width}}".format(fib_type.title(), width=col_width)
        duration = details[0]
        for precision in precisions:
            row += "{:>{width}}".format(duration_format(duration, precision), width=col_width + 1)


def write_to_file(fib_details: dict):
    """Function to write information to file."""
    #loop through all fibonacci method and sequence values list pair,
    for fib_type, details in fib_details.items():
        #create path using filename ss the method name with space replace with '_' and .txt extension added
        file_path = RESOURCES / "{}.txt".format(fib_type.replace(" ", "_"))
        #Open file in write mode and
        with open(file_path, 'w') as file:
            #zip list of numbers from the length of the list -1 down to zero, to the list of fibonacci values
            #write each zipped pair to a new lin in the file with a space after ':'
            for idx, value in zip(range(len(details[1]) - 1, -1, -1), details[1]):
                file.write("{}: {}\n".format(idx, value))


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT179G Assignment 3 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('nth', metavar='nth', type=int, nargs='?', default=30,
                        help="nth Fibonacci sequence to find.")

    global LOGGER  # ignore warnings raised from linters, such as PyLint!
    LOGGER = create_logger()

    args = parser.parse_args()
    nth_value = args.nth  # nth value to sequence. Will fallback on default value!

    fib_details = {  # store measurement information in a dictionary
        'fib iteration': fibonacci_iterative(nth_value),
        'fib recursion': fibonacci_recursive(nth_value),
        'fib memory': fibonacci_memory(nth_value)
    }

    print_statistics(fib_details, nth_value)  # print information in console
    write_to_file(fib_details)  # write data files


if __name__ == "__main__":
    main()
