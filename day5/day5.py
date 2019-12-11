import copy
from collections import deque
from enum import IntEnum
from typing import Tuple, Any, List


# Solution for: https://adventofcode.com/2019/day/5
class IntcodeComputer:
    def __init__(self, instruction_file, buffered_inputs=None):
        self.memory_mapping = {i: int(int_codes.split(sep=',')[i]) for int_codes in instruction_file for i in
                               range(len(int_codes.split(sep=',')))}
        self.__initial_memory_mapping = copy.deepcopy(self.memory_mapping)
        if buffered_inputs is None:
            buffered_inputs = []
        self.buffered_inputs = deque(buffered_inputs)
        self.instruction_pointer = 0
        self.relative_offset = 0

    def reset(self, buffered_inputs=None):
        self.memory_mapping = copy.deepcopy(self.__initial_memory_mapping)
        if buffered_inputs is None:
            buffered_inputs = []
        self.buffered_inputs = deque(buffered_inputs)
        self.instruction_pointer = 0

    def fetch_arguments(self, number_of_arguments: int, modes: List[int],
                        contains_write_to_address: bool = False) -> Tuple:
        arguments = []

        # Fetch
        for i in range(1, number_of_arguments + 1):
            # Fetch
            argument = self.memory_mapping.get(self.instruction_pointer + i, 0)
            parameter_mode = modes[i - 1]

            # Translate
            if i < number_of_arguments:
                # Read-to-addresses can be resolved directly
                if parameter_mode == ParameterMode.POSITION_MODE:
                    resolved_argument = self.memory_mapping.get(argument, 0)
                elif parameter_mode == ParameterMode.IMMEDIATE_MODE:
                    resolved_argument = argument
                else:
                    resolved_argument = self.memory_mapping.get(argument + self.relative_offset, 0)
            else:
                if contains_write_to_address:
                    # Write-to-addresses need to be resolved at writing time
                    if parameter_mode == ParameterMode.RELATIVE_MODE:
                        resolved_argument = argument + self.relative_offset
                    else:
                        resolved_argument = argument
                else:
                    if parameter_mode == ParameterMode.POSITION_MODE:
                        resolved_argument = self.memory_mapping.get(argument, 0)
                    elif parameter_mode == ParameterMode.IMMEDIATE_MODE:
                        resolved_argument = argument
                    else:
                        resolved_argument = self.memory_mapping.get(argument + self.relative_offset, 0)

            # Append
            arguments.append(resolved_argument)

        return tuple(arguments)

    def process_next_instruction(self) -> Tuple[bool, Any]:
        next_instruction_pointer = self.instruction_pointer

        instruction = self.memory_mapping.get(self.instruction_pointer, 0)

        instruction_string = '0' * (5 - len(str(instruction))) + str(instruction)
        parameter_modes = [int(instruction_string[-3:-2]), int(instruction_string[-4:-3]), int(instruction_string[-5:-4])]
        opcode = int(instruction_string[-2:])

        return_value = None

        # Fetch arguments
        tar = None
        arg_1 = None
        arg_2 = None
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            arg_1, arg_2, tar = self.fetch_arguments(3, parameter_modes, True)
        elif opcode == 3:
            tar, = self.fetch_arguments(1, parameter_modes, True)
        elif opcode == 4:
            tar, = self.fetch_arguments(1, parameter_modes)
        elif opcode == 5 or opcode == 6:
            arg_1, arg_2 = self.fetch_arguments(2, parameter_modes)
        elif opcode == 9:
            arg_1 = self.fetch_arguments(1, parameter_modes)[0]

        # Apply opcode
        if opcode == 1:
            self.memory_mapping[tar] = arg_1 + arg_2

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 2:
            self.memory_mapping[tar] = arg_1 * arg_2

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 3:
            if len(self.buffered_inputs) > 0:
                self.memory_mapping[tar] = self.buffered_inputs.popleft()
            else:
                self.memory_mapping[tar] = int(input('Please enter input: '))

            # Set next instruction pointer
            next_instruction_pointer += 2
        elif opcode == 4:
            return_value = tar
            print(return_value)

            # Set next instruction pointer
            next_instruction_pointer += 2
        elif opcode == 5:
            if arg_1 != 0:
                next_instruction_pointer = arg_2
            else:
                # Set next instruction pointer if not jumpy
                next_instruction_pointer += 3
        elif opcode == 6:
            if arg_1 == 0:
                next_instruction_pointer = arg_2
            else:
                # Set next instruction pointer if not jumped
                next_instruction_pointer += 3
        elif opcode == 7:
            if arg_1 < arg_2:
                self.memory_mapping[tar] = 1
            else:
                self.memory_mapping[tar] = 0

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 8:
            if arg_1 == arg_2:
                self.memory_mapping[tar] = 1
            else:
                self.memory_mapping[tar] = 0

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 9:
            self.relative_offset += arg_1

            # Set next instruction pointer
            next_instruction_pointer += 2
        elif opcode == 99:
            return True, return_value

        self.instruction_pointer = next_instruction_pointer

        return False, return_value


class ParameterMode(IntEnum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2


def run_diagnostic_program():
    with open('input.txt', mode='r') as int_code_file:
        int_code_computer = IntcodeComputer(int_code_file)

        halted, _ = int_code_computer.process_next_instruction()
        while not halted:
            halted, _ = int_code_computer.process_next_instruction()


if __name__ == '__main__':
    run_diagnostic_program()
