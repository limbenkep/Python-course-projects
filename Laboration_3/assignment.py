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
    """Create and return custom logger object.
    The logger is set t DEBUG level
    a console handler with level set to INFO
    and a file handler set to DEBUG level logging to a file ass_3.log opened on write mode
     are added to the logger.
    Both hanlers have custom formatting"""

    #logger can also be created by reading from file (teacher's feedback)
    #with open(RESOURCES / "ass3_log_conf.json") as file:
        #logging.config.dictConfig(json.load(file))
        #return logging.getLogger('ass_3_logger')
    logger = logging.getLogger("ass_3_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    log_path = RESOURCES / "ass_3.log"
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setLevel(logging.DEBUG)

    console_format = logging.Formatter("%(levelname)s | %(message)s")
    file_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def measurements_decorator(func):
    """Function decorator, used for time measurements.
    The decorator makes use of a wrapper that starts a timer and
    log a message to logger at INFO level at the beginning of the measurement,
    gets the number nth_nmb from the func parameter list and
     loops through numbers from the nth_nmb to zero, run func for each of the numbers
     and store the result in a list,
      for every fifth iteration, the number and result is logged at debug level.
      return the time taken for the computation and the list of results as a tuple"""

    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:
        result = list()
        start_time = timer()
        LOGGER.info("Starting measurements...{}".format(func.__name__))
        counter = 0
        for nth_nmb in range(nth_nmb, -1, -1):
            result.append(func(nth_nmb))
            if counter % 5 == 0:
                LOGGER.debug("{}: {}".format(nth_nmb, result[counter]))
            counter += 1
        duration = timer() - start_time
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


memory = {0: 0, 1: 1}


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """Computes Fibonacci value using recursive method. Has a dictionary to which call
    computed fibonacci value computed are store in as number:fib value.
    Check if fibonacci value has already been computed and stored to dictionary,
     if found in list use value, if not found compute value and store in in dictionary.
     return the fibonacci value."""

    def fib_memory(n):
        if n in memory:
            return memory[n]
        memory[n] = fib_memory(n - 1) + fib_memory(n - 2)
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
    """Function which handles printing to console.
    formats printout and prints computation time for the different methods in
    seconds, milliseconds, microseconds and nanoseconds with header"""
    line = '\n' + ("---------------" * 5)
    print_title = "DURATION FOR EACH APPROACH WITHIN INTERVAL: " + str(nth_value) + "-0"
    print("{:<75}\n{:^75}{:<75}".format(line, print_title, line))
    print("{:<15}  {:>15}  {:>15}  {:>15}  {:>15}".format("", "Seconds", "Milliseconds", "Microseconds",
                                                          "Nanoseconds"))
    for key in fib_details:
        results = fib_details[key]
        duration = results[0]
        print("{:<15}  {:>15}  {:>15}  {:>15}  {:>15}".format(key.title(), duration_format(duration, "Seconds"),
                                                              duration_format(duration, "Milliseconds"),
                                                              duration_format(duration, "Microseconds"),
                                                              duration_format(duration, "Nanoseconds")))


def write_to_file(fib_details: dict):
    """Function to write information to file.
    for each fibonacci method and sequence values list pair,
    create and open a file on write mode with the where the
    filename is the method name with space replace with '_' and .txt extension added
     zip list of numbers from the length of the list -1 down to zero, to the list of fibonacci values,
      write each zipped pair to a new lin in the file with a space after ':'"""

    for fib_type, details in fib_details.items():
        file_path = RESOURCES / "{}.txt".format(fib_type.replace(" ", "_"))
        with open(file_path, 'w') as file:
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
