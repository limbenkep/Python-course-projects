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
import itertools
import sys
import time
from pathlib import Path
from ast import literal_eval
from time import sleep
import os
import code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """
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

    def parse_world_size_form_file(file_data):
        """Checks and returns world size if world size data is a list of two integers else raise exception"""
        try:
            """TypeError generated if data["world_size"] is not a list of size 2 """
            [width, height] = file_data["world_size"]
            """TypeError generated if width or height is not an integers"""
            if width < 1 or height < 1:
                raise ValueError("Both width and height has to be positive values above zero.")
            return width, height
        except TypeError as e:
            print("World size should be a list containing two integers corresponding to width and height")
            sys.exit()
        except ValueError as e:
            print(e)
            sys.exit()
        except Exception as e:
            print(e)
            sys.exit()

    def parse_coordinates_from_file(coordinate_str, world_size):
        """Checks if coordinates is tuple with two int and if values conforms with world size"""
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

    def parse_cell_object_from_file(cell_object, world_size):
        """Checks and returns cell object if it conforms to expected data or raise exception"""
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

    def parse_population_from_file(file_data, world_size):
        try:
            population = file_data["population"]
            # print(type(population))
            cells_world = {}
            if not isinstance(population, dict):
                raise TypeError("World population should a dictionary")
            for key, value in population.items():
                coordinate = parse_coordinates_from_file(key, world_size)
                # cell = population[coordinate]
                cells_world[coordinate] = parse_cell_object_from_file(value, world_size)
            return cells_world
        except KeyError as e:
            print("Key 'population' should be used to map population")
            print(20 * "*" + "\nPrinting KeyError")
            print(str(e))
            sys.exit()
        except TypeError as e:
            print(20 * "*" + "\nPrinting TypeError")
            print(str(e))
            sys.exit()
        except Exception as e:
            print(20 * "*" + "\nPrinting Exception")
            print(str(e))
            sys.exit()

    def parse_neighbours_from_file(neighbours, world_size):
        try:
            (width, height) = world_size
            new_list = []
            if not isinstance(neighbours, list):
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

    with open(path, 'r') as file:
        data = json.load(file)
        size = parse_world_size_form_file(data)
        print("size: {}".format(size))
        world = parse_population_from_file(data, size)
        print(f"Value of world={world} and has size {size}")
        return world, size


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    pass


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    pass


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """
    values = _arg.split("x")
    try:
        assert len(values) == 2, "World size should contain width and length, seperated by 'x', Ex: '80x40'."

        width = int(values[0])
        height = int(values[1])

        if width < 1 or height < 1:
            raise ValueError("Both width and height has to be positive values above zero."
                             "\nUsing default world size : 80x40")
        return width, height
    except AssertionError as e:
        print(e)
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
    """ Populate  return the world with cells and initial states. """
    width = _world_size[0]
    height = _world_size[1]

    def swap_coordinate_points(pattern: list):
        return [(val[1], val[0]) for val in pattern]

    def get_cell_state(position):
        """Determine the state of cell from pattern or by randomization and return it
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
            return {state: neighbours}

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


def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """
    current_population = _population

    for val in range(_generations):
        cb.clear_console()
        new_population = update_world(current_population, _world_size)
        current_population = new_population
        time.sleep(0.2)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation.
    Prints current generation and generate and returns next generation """

    def get_cell_next_state(position: tuple):
        """Determine cell state for next generation from current cell state and state of neighbours
        Any live cell with two or three live neighbours survives.
        Any dead cell with three live neighbours becomes a live cell.
        All other live cells die in the next generation.
        all other dead cells stay dead."""
        _cell_object = _cur_gen[position]
        [(_state, _neighbours)] = _cell_object.items()
        live_neighbour = count_alive_neighbours(_neighbours, _cur_gen)
        if state == cb.STATE_ALIVE and live_neighbour == 2:
            return cb.STATE_ALIVE
        elif state == cb.STATE_ALIVE and live_neighbour == 3:
            return cb.STATE_ALIVE
        elif state == cb.STATE_DEAD and live_neighbour == 3:
            return cb.STATE_ALIVE
        else:
            return cb.STATE_DEAD

    width = _world_size[0]
    height = _world_size[1]
    next_generation = {}
    """for cell in every position in world, print current cell state, determine state for next generation 
    and store a copy of cell with updated state for next generation """
    for y in range(height):
        for x in range(width):
            key = (y, x)
            if is_rim_cell(key, _world_size):
                cb.progress(cb.get_print_value(cb.STATE_RIM))
                next_generation[key] = None
            else:
                cell_object = _cur_gen[key]
                [(state, neighbours)] = cell_object.items()
                cb.progress(cb.get_print_value(state))
                next_generation[key] = {get_cell_next_state(key): neighbours}
        print("")
    return next_generation


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive."""
    live_cell = 0
    for val in _neighbours:
        cell_object = _cells[val]
        """if cell is noto a rim-cell"""
        if cell_object is not None:
            [state] = cell_object.keys()
            if state == cb.STATE_ALIVE:
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
