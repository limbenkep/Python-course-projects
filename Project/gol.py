#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import pathlib
import random
import json
import logging
import sys
from pathlib import Path
from ast import literal_eval
from time import sleep
import code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def parse_world_size_form_file(world_size_data):
    """Receives world size read from file as a List,
     check if list contains exactly two integers each greater than zero
     extract width and height and return them as a tuple which is the
     expected format to be used in world population
     or raise exception if and exit if validation fails"""
    try:
        """TypeError generated if data["world_size"] is not a list of size 2 """
        [width, height] = world_size_data["world_size"]
        """TypeError generated if width or height is not an integers"""
        if width < 1 or height < 1:
            raise ValueError("Both width and height needs to have "
                             "positive values above zero.")
        return width, height
    except TypeError:
        print("World size should be a list containing two "
              "integers corresponding to width and height")
        sys.exit()
    except ValueError as e:
        print(e)
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()


def parse_coordinates_from_file(coordinate_str, world_size):
    """Receives coordinates read from file as a string and convert it to a tuple,
     then check if coordinates are two  integers and
    if values falls within the expected range for the given world size"""
    try:
        [width, height] = world_size
        coordinate = literal_eval(coordinate_str)
        (y, x) = coordinate
        if y < 0 or x < 0 or x > width - 1 or y > height - 1:
            raise ValueError("Coordinate values out of bounds")
        return y, x
    except TypeError:
        print("Coordinates should be in format (y, x) where x and y are integers")
        sys.exit()
    except ValueError as e:
        sys.exit(str(e))
    except Exception as e:
        sys.exit(str(e))


def parse_neighbours_from_file(neighbours, world_size):
    """Receives neighbours data read from file as a list,
     Check if the read data is a list of 8 elements ,
     and if each element is a list of 2 integers greater than zero
     and lies within the expected range for the given world size
      store each neighbour as a tuple return a list of all neighbours"""
    try:
        (width, height) = world_size
        new_list = []
        if not isinstance(neighbours, list) or len(neighbours) != 8:
            raise TypeError("Neighbours should be a list of coordinates with format (x, Y) "
                            "where x and y are integers")
        for coordinate in neighbours:
            if len(coordinate) != 2:
                raise TypeError("Neighbours coordinates should be two integers")
            y = coordinate[0]
            x = coordinate[1]
            if y < 0 or x < 0 or x > width - 1 or y > height:
                raise ValueError("Coordinate values out of bounds")
            new_list.append((y, x))
        return new_list
    except TypeError as e:
        sys.exit(str(e))
    except ValueError as e:
        print(e)
        sys.exit(str(e))
    except Exception as e:
        print(e)
        sys.exit(str(e))


def parse_cell_object_from_file(cell_object, world_size):
    """receives data read from file corresponding to cell details,
    check that the read data is a dictionary,
    extract data for cell state and compare to expected values,
    extract data for neighbours and call function to parse neighbours
    return state and neighbour as a key:value pair
    raise exception and exit"""
    try:
        if not isinstance(cell_object, dict) and cell_object is not None:
            raise TypeError("Cell coordinates should be map a dictionary containing state "
                            "and neighbours or none.")
        if cell_object is None:
            return None
        state = cell_object["state"]
        neighbours = cell_object["neighbours"]
        new_cell_object = {}
        if not isinstance(state, str):
            raise TypeError("State should be a string")
        if state is not cb.STATE_ALIVE and state is not cb.STATE_DEAD and state is not cb.STATE_RIM:
            raise ValueError("Invalid state value. The values should be'#' or '-' or 'x'.")
        if not isinstance(neighbours, list):
            raise TypeError("Neighbours should be a list of coordinates of neighbouring cells")
        new_cell_object[state] = parse_neighbours_from_file(neighbours, world_size)
        new_cell_object["age"] = 0
        return new_cell_object
    except KeyError:
        print("Key 'state' should cell state and 'neighbour should map cell neighbours")
        sys.exit()
    except TypeError as e:
        print(str(e))
        sys.exit()
    except ValueError as e:
        print(str(e))
        sys.exit()
    except Exception as e:
        print(str(e))
        sys.exit()


def parse_population_from_file(file_data: dict, world_size: tuple) -> dict:
    """Receives data read form file.
    Get data for cell population using key 'population'
    which throws keyError exception if key not found,
    check that population is a dictionary,
    for every key:value pair, key is coordinate data which is parsed
    by calling function parse_coordinates_from_file,
    and value contain cell details which is parsed by calling method
    parse_cell_object_from_file
    all parsed coordinate:cell details pairs are stored in a dictionary and returned """
    try:
        population = file_data["population"]
        parsed_population = {}
        if not isinstance(population, dict):
            raise TypeError("World population should a dictionary")
        for key, value in population.items():
            coordinate = parse_coordinates_from_file(key, world_size)
            parsed_population[coordinate] = parse_cell_object_from_file(value, world_size)
        return parsed_population
    except KeyError as e:
        print("Key 'population' should be used to map population")
        print(str(e))
        sys.exit()
    except TypeError as e:
        print(str(e))
        sys.exit()
    except Exception as e:
        print(str(e))
        sys.exit()


def load_seed_from_file(_file_name: str) -> tuple:
    """ Read population seed from file.
    check if data is of correct type, if not throw exception,
    print error message end program.
    Else parse data and store in a dictionary in the expected format for world.
    Returns tuple: population (dict) and world_size (tuple). """

    length = len(_file_name)
    if length < 5:
        _file_name = _file_name + ".json"
    else:
        last_five = _file_name[-5:]
        print("Printing last five characters", last_five)
        if last_five == ".json":
            _file_name = _file_name
        else:
            _file_name = _file_name + ".json"

    path = pathlib.Path.home() / RESOURCES / _file_name
    print(f"The file to read is  {_file_name} with path {path}")
    with open(path, 'r') as file:
        data = json.load(file)
        size = parse_world_size_form_file(data)
        print("size: {}".format(size))
        world = parse_population_from_file(data, size)
        print(f"Value of world={world} and has size {size}")
        return world, size


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    logger = logging.getLogger("gol_logger")
    logger.setLevel(logging.INFO)

    log_path = pathlib.Path.home() / RESOURCES / "gol.log"
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    logger = create_logger()

    def wrapper(*args):
        """number of rim cells is the same for all generations,
        so count all rim cells by checking the state for each cell,
        then loop for the number of generations given.
        For each generation get new generation by calling func which will be
        run_simulation function that prints current generation and returns next generation,
        count live, elder, prime_elder and dead cells ,
        log data and new generation becomes current generation for the next generation

        """
        current_population = args[1]
        ordinary_cells = 0
        for coordinate in current_population.keys():
            if not is_rim_cell(coordinate, args[2]):
                ordinary_cells += 1
        for val in range(args[0]):
            cb.clear_console()
            new_population = func(args[0], current_population, args[2])

            live_count = 0
            dead_count = 0
            elder_count = 0
            prime_elder_count = 0
            for key, value in current_population.items():
                if value is not None:
                    state = get_state_from_cell_details(value)
                    if state == cb.STATE_ALIVE:
                        live_count += 1
                    if state == cb.STATE_DEAD:
                        dead_count += 1
                    if state == cb.STATE_ELDER:
                        elder_count += 1
                    if state == cb.STATE_PRIME_ELDER:
                        prime_elder_count += 1

            logger.info("GENERATION {}\n  Population: {}\n  Alive: {}\n  Elders: {}\n  Prime Elders: {}\n  Dead: {}"
                        .format(val, ordinary_cells, live_count + elder_count + prime_elder_count, elder_count,
                                prime_elder_count, dead_count))
            current_population = new_population
            sleep(0.2)
    return wrapper


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    values = _arg.split("x")
    try:
        """Check if list result from contain exactly two elements; width and height"""
        assert len(values) == 2, "World size should contain width and length, " \
                                 "seperated by 'x', Ex: '80x40'."
        """Conversion to int will through throw an valueError exception if any of the 
        values are not numbers"""
        width = int(values[0])
        height = int(values[1])
        """Check if width and height are greater than zero"""
        if width < 1 or height < 1:
            raise ValueError("Both width and height needs to have positive values above zero.")
        return width, height
    except AssertionError as e:
        print("{}\nUsing default world size : 80x40".format(e))
        return 80, 40
    except ValueError as e:
        print("{}\nUsing default world size : 80x40".format(e))
        return 80, 40
    except Exception as e:
        print("{}\nUsing default world size : 80x40".format(e))
        return 80, 40


def is_rim_cell(_position: tuple, _world_size: tuple):
    """Check and returns true if cell is a rim cell else returns false"""
    width = _world_size[0]
    height = _world_size[1]
    y = _position[0]
    x = _position[1]
    """check if cell's row or column is the world's first or last row or column """
    if x == 0 or y == 0 or x == (width - 1) or y == (height - 1):
        return True
    return False


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ This function populate return the world with seed population.
     two helper inner functions are used here for readability and to avoid nesting at multiple levels.
     Here the format of the coordinate is (y,x) format to match the format used in provided patterns"""
    width = _world_size[0]
    height = _world_size[1]

    def get_cell_state(position):
        """Determine the state of a cell.
         Check if cell is a rim cell by calling function is_rim_cell if so return STATE_RIM,
         get pattern, returns a list of coordinates if _seed_pattern is one of the predefined patterns
         or None if the given pattern is unknown or if no pattern was passed.
         if pattern is None get a random integer and
         if the integer is greater than 16 return STATE_ALIVE else return STATE_DEAD
        else check if coordinate is found in the list returned by get_pattern, if yes return STATE_ALIVE
        else return STATE_DEAD
        cells state are determined from pattern if given or by randomisation if pattern is not given"""
        if is_rim_cell(position, _world_size):
            return cb.STATE_RIM
        pattern = cb.get_pattern(_seed_pattern, _world_size)
        if pattern is None:
            random.seed()
            if random.randint(0, 20) > 16:
                return cb.STATE_ALIVE
            return cb.STATE_DEAD
        else:
            if position in pattern:
                return cb.STATE_ALIVE
            return cb.STATE_DEAD

    def get_cell_object(position):
        """return a dictionary with the cell state mapped to a list of the
        cell's neighbours or None if cell is rim cell"""
        if is_rim_cell(position, _world_size):
            return None
        else:
            neighbours = calc_neighbour_positions(position)
            state = get_cell_state(position)
            return {state: neighbours, "age": 0}

    """Map world positions to corresponding cell objects and return world"""
    world = {}
    for x in range(width):
        for y in range(height):
            world[(y, x)] = get_cell_object((y, x))
    return world


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """
    neighbours = []
    row = _cell_coord[0]
    column = _cell_coord[1]
    """calculate NW neighbour"""
    neighbours.append((row - 1, column - 1))
    """calculate N neighbour"""
    neighbours.append((row - 1, column))
    """calculate NE neighbour"""
    neighbours.append((row - 1, column + 1))
    """calculate W neighbour"""
    neighbours.append((row, column - 1))
    """calculate E neighbour"""
    neighbours.append((row, column + 1))
    """calculate SW neighbour"""
    neighbours.append((row + 1, column - 1))
    """calculate S neighbour"""
    neighbours.append((row + 1, column))
    """calculate SE neighbour"""
    neighbours.append((row + 1, column + 1))

    return neighbours


def get_state_from_cell_details(_cell_details):
    """get state key by get the key that is not 'age'"""
    for key in _cell_details.keys():
        if key is not "age":
            return key


@simulation_decorator
def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Encapsulates the update_world function and Represents a tick in the simulation. """
    return update_world(_population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation.
    Prints current generation and generate and returns next generation """

    def get_cell_next_state(position: tuple):
        """Determine cell state for next generation from current cell state and state of neighbours,
        and update age by adding 1 to age value if cell is alive and assigning zero to age if dead
        Any live cell with two or three live neighbours survives.
        Any dead cell with three live neighbours becomes a live cell.
        All other live cells die in the next generation.
        all other dead cells stay dead.
        For live if age >5 state is STATE_ELDER, if age >10 state is STATE_PRIME_ELDER"""
        _cell_object = _cur_gen[position]
        _state = get_state_from_cell_details(_cell_object)
        _neighbours = _cell_object[_state]
        live_neighbour = count_alive_neighbours(_neighbours, _cur_gen)
        if _state == cb.STATE_ALIVE and live_neighbour == 2:
            age = _cell_object["age"] + 1
            if age > 5:
                return cb.STATE_ELDER, age
            return cb.STATE_ALIVE, age
        elif _state == cb.STATE_ALIVE and live_neighbour == 3:
            age = _cell_object["age"] + 1
            if age > 5:
                return cb.STATE_ELDER, age
            return cb.STATE_ALIVE, age
        elif _state == cb.STATE_ELDER and live_neighbour == 2:
            age = _cell_object["age"] + 1
            if age > 10:
                return cb.STATE_PRIME_ELDER, age
            return cb.STATE_ELDER, age
        elif _state == cb.STATE_ELDER and live_neighbour == 3:
            age = _cell_object["age"] + 1
            if age > 10:
                return cb.STATE_PRIME_ELDER, age
            return cb.STATE_ELDER, age
        elif _state == cb.STATE_PRIME_ELDER and live_neighbour == 2:
            age = _cell_object["age"] + 1
            return cb.STATE_PRIME_ELDER, age
        elif _state == cb.STATE_PRIME_ELDER and live_neighbour == 3:
            age = _cell_object["age"] + 1
            return cb.STATE_PRIME_ELDER, age
        elif _state == cb.STATE_DEAD and live_neighbour == 3:
            age = _cell_object["age"] + 1
            return cb.STATE_ALIVE, age
        else:
            return cb.STATE_DEAD, 0

    width = _world_size[0]
    height = _world_size[1]
    next_generation = {}
    """for cell in every position in world, print current cell state, 
    determine state for next generation,
    store a copy of cell with updated state for next generation to a new dictionary and 
    return the new dictionary. """
    for y in range(height):
        for x in range(width):
            coordinate = (y, x)
            if is_rim_cell(coordinate, _world_size):
                cb.progress(cb.get_print_value(cb.STATE_RIM))
                next_generation[coordinate] = None
            else:
                cell_object = _cur_gen[coordinate]
                state = get_state_from_cell_details(cell_object)
                cb.progress(cb.get_print_value(state))
                neighbours = cell_object[state]
                (new_state, new_age) = get_cell_next_state(coordinate)
                next_generation[coordinate] = {new_state: neighbours, "age": new_age}
        print("")
    return next_generation


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive.
    Start counter live_cell at 0
    For each cell in _neighbours, check that the cell is not a rim cell because
    rim cells cell has a None value for cell_object and .keys() operation on a
    None value will generate an error.
    If cell is not a rim cell, check if cell state is STATE_ALIVE or STATE_ELDER, or STATE_PRIME_ELDER
    if yes, increase counter live_cell by 1"""
    live_cell = 0
    for val in _neighbours:
        cell_object = _cells[val]
        """if cell is not a rim-cell"""
        if cell_object is not None:
            state = get_state_from_cell_details(cell_object)
            if state == cb.STATE_ALIVE or state == cb.STATE_ELDER or state == cb.STATE_PRIME_ELDER:
                live_cell += 1
    return live_cell


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
