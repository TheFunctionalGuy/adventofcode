from enum import IntEnum
from typing import Dict, Tuple

from termcolor import colored

from day5.day5 import IntcodeComputer


# Solution for: https://adventofcode.com/2019/day/11
def build_emergency_hull_painting_robot():
    with open('input.txt', mode='r') as program_file:
        # Part one
        int_code_computer = IntcodeComputer(program_file)
        first_paint_mapping = run_robot(int_code_computer, Color.BLACK)

        print(f'The emergency hull painting robot does visit {len(first_paint_mapping)} panels at least once.')

        # Part two
        second_paint_mapping = run_robot(int_code_computer, Color.WHITE)
        render_painting(second_paint_mapping)


def run_robot(int_code_computer, initial_color: int) -> Dict[Tuple[int, int], int]:
    int_code_computer.reset()
    start_position = (0, 0)
    start_direction = Direction.UP
    paint_mapping = {}

    halted = False
    current_position = start_position
    current_direction = start_direction
    int_code_computer.add_input(initial_color)

    while not halted:
        color = None
        while color is None and not halted:
            halted, color = int_code_computer.process_next_instruction()

        direction = None
        while direction is None and not halted:
            halted, direction = int_code_computer.process_next_instruction()

        # Paint current panel
        if color is not None:
            paint_mapping[current_position] = color

        # Get next orientation
        if direction == 0:
            current_direction = (current_direction - 1) % 4
        else:
            current_direction = (current_direction + 1) % 4

        # Move one panel forward
        if current_direction == Direction.UP:
            current_position = (current_position[0], current_position[1] + 1)
        elif current_direction == Direction.RIGHT:
            current_position = (current_position[0] + 1, current_position[1])
        elif current_direction == Direction.DOWN:
            current_position = (current_position[0], current_position[1] - 1)
        else:
            current_position = (current_position[0] - 1, current_position[1])

        int_code_computer.add_input(paint_mapping.get(current_position, Color.BLACK))

    return paint_mapping


def render_painting(paint_mapping: Dict[Tuple[int, int], int]):
    highest_x_value = None
    lowest_x_value = None
    highest_y_value = None
    lowest_y_value = None

    for x, y in paint_mapping:
        if highest_x_value is None or highest_x_value < x:
            highest_x_value = x
        if lowest_x_value is None or lowest_x_value > x:
            lowest_x_value = x
        if highest_y_value is None or highest_y_value < y:
            highest_y_value = y
        if lowest_y_value is None or lowest_y_value > y:
            lowest_y_value = y

    print('Painted registration identifier:')
    for y in range(0, -6, -1):
        for x in range(0, 43):
            if paint_mapping.get((x, y), Color.BLACK) == Color.WHITE:
                print(colored('\u2588', 'blue'), end='')
            else:
                print(colored('\u2588', 'yellow'), end='')
        print()


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


if __name__ == '__main__':
    build_emergency_hull_painting_robot()
