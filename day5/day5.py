from typing import Tuple


# Solution for: https://adventofcode.com/2019/day/5
class IntcodeComputer:
    def __init__(self, instruction_file, diagnostic_input):
        self.instructions = [int(int_code) for int_codes in instruction_file for int_code in
                             int_codes.rstrip().split(sep=',')]
        self.diagnostic_input = diagnostic_input
        self.instruction_pointer = 0

    def fetch_arguments(self, number_of_arguments: int) -> Tuple:
        arguments = []
        for i in range(1, number_of_arguments + 1):
            # Fetch
            argument = self.instructions[self.instruction_pointer + i]
            # Append
            arguments.append(argument)

        return tuple(arguments)

    def execute_operation_1(self, arg_1: int, arg_2: int, tar: int):
        pass

    def process_next_instruction(self) -> bool:
        next_instruction_pointer = self.instruction_pointer

        opcode = self.instructions[self.instruction_pointer]

        instruction_string = '0' * (5 - len(str(opcode))) + str(opcode)
        mode_1 = bool(int(instruction_string[-3:-2]))
        mode_2 = bool(int(instruction_string[-4:-3]))
        mode_3 = bool(int(instruction_string[-5:-4]))
        opcode = int(instruction_string[-2:])

        # Fetch arguments
        tar = None
        arg_1 = None
        arg_2 = None
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            # Fetch arguments
            arg_1, arg_2, tar = self.fetch_arguments(3)

            if not mode_1:
                arg_1 = self.instructions[arg_1]
            if not mode_2:
                arg_2 = self.instructions[arg_2]
        elif opcode == 3:
            tar = self.fetch_arguments(1)[0]
        elif opcode == 4:
            tar = self.fetch_arguments(1)[0]

            if not mode_1:
                tar = self.instructions[tar]
        elif opcode == 5 or opcode == 6:
            arg_1, arg_2 = self.fetch_arguments(2)

            if not mode_1:
                arg_1 = self.instructions[arg_1]
            if not mode_2:
                arg_2 = self.instructions[arg_2]

        if opcode == 1:
            # Apply opcode
            self.instructions[tar] = arg_1 + arg_2

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 2:
            # Apply opcode
            self.instructions[tar] = arg_1 * arg_2

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 3:
            # Apply opcode
            self.instructions[tar] = self.diagnostic_input

            # Set next instruction pointer
            next_instruction_pointer += 2
        elif opcode == 4:
            # Apply opcode
            print(tar)

            # Set next instruction pointer
            next_instruction_pointer += 2
        elif opcode == 5:
            # Apply opcode
            if arg_1 != 0:
                next_instruction_pointer = arg_2
            else:
                # Set next instruction pointer if not jumpy
                next_instruction_pointer += 3
        elif opcode == 6:
            # Apply opcode
            if arg_1 == 0:
                next_instruction_pointer = arg_2
            else:
                # Set next instruction pointer if not jumped
                next_instruction_pointer += 3
        elif opcode == 7:
            if arg_1 < arg_2:
                self.instructions[tar] = 1
            else:
                self.instructions[tar] = 0

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 8:
            if arg_1 == arg_2:
                self.instructions[tar] = 1
            else:
                self.instructions[tar] = 0

            # Set next instruction pointer
            next_instruction_pointer += 4
        elif opcode == 99:
            return True

        self.instruction_pointer = next_instruction_pointer

        return False


def run_diagnostic_program():
    diagnostic_input = input('Please enter diagnostic program input: ')

    with open('input.txt', mode='r') as int_code_file:
        int_code_computer = IntcodeComputer(int_code_file, int(diagnostic_input))

        halted = int_code_computer.process_next_instruction()
        while not halted:
            halted = int_code_computer.process_next_instruction()


if __name__ == '__main__':
    run_diagnostic_program()
