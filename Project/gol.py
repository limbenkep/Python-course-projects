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
import random
import json
import logging
import itertools
import time
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

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """
    pass


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
    print(values)
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
        return [(val[1],val[0]) for val in pattern]

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
