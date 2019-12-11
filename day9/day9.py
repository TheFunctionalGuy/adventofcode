from day5.day5 import IntcodeComputer


# Solution for: https://adventofcode.com/2019/day/9
def execute_boost_program():
    with open('input.txt', mode='r') as boost_program_file:
        int_code_computer = IntcodeComputer(boost_program_file)

        halted, ret = int_code_computer.process_next_instruction()
        while not halted:
            halted, ret = int_code_computer.process_next_instruction()


if __name__ == '__main__':
    execute_boost_program()
