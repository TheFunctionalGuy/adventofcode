import copy
import itertools

from day5.day5 import IntcodeComputer


# Solution for: https://adventofcode.com/2019/day/7
def run_amplifier_controller_software():
    with open('input.txt', mode='r') as controller_software_file:
        # Part one
        int_code_computer = IntcodeComputer(controller_software_file)

        thruster_signals = []

        for inputs in itertools.permutations(range(5), 5):
            int_code_computer.reset([inputs[0], 0])
            halted, ret = int_code_computer.process_next_instruction()

            while ret is None and not halted:
                halted, ret = int_code_computer.process_next_instruction()

            for i in range(4):
                int_code_computer.reset([inputs[i + 1], ret])

                halted, ret = int_code_computer.process_next_instruction()
                while ret is None and not halted:
                    halted, ret = int_code_computer.process_next_instruction()

            thruster_signals.append(ret)

        maximum_signal = sorted(thruster_signals, reverse=True)[0]

        print(f'Maximum thruster signal is: {maximum_signal}')

        # Part two
        thruster_signals_with_feedback_loop = []

        for inputs in itertools.permutations(range(5, 10), 5):
            int_code_computer.reset()
            int_code_computer_a = copy.deepcopy(int_code_computer)
            int_code_computer_b = copy.deepcopy(int_code_computer)
            int_code_computer_c = copy.deepcopy(int_code_computer)
            int_code_computer_d = copy.deepcopy(int_code_computer)
            int_code_computer_e = copy.deepcopy(int_code_computer)

            int_code_computer_a.add_input(inputs[0])
            int_code_computer_a.add_input(0)
            int_code_computer_b.add_input(inputs[1])
            int_code_computer_c.add_input(inputs[2])
            int_code_computer_d.add_input(inputs[3])
            int_code_computer_e.add_input(inputs[4])

            e_halted = False
            e_ret = None
            last_e_ret = None

            # Feedback loop
            while not e_halted:
                a_halted, a_ret = int_code_computer_a.process_next_instruction()
                while a_ret is None and not a_halted:
                    a_halted, a_ret = int_code_computer_a.process_next_instruction()

                int_code_computer_b.add_input(a_ret)

                b_halted, b_ret = int_code_computer_b.process_next_instruction()
                while b_ret is None and not b_halted:
                    b_halted, b_ret = int_code_computer_b.process_next_instruction()

                int_code_computer_c.add_input(b_ret)

                c_halted, c_ret = int_code_computer_c.process_next_instruction()
                while c_ret is None and not c_halted:
                    c_halted, c_ret = int_code_computer_c.process_next_instruction()

                int_code_computer_d.add_input(c_ret)

                d_halted, d_ret = int_code_computer_d.process_next_instruction()
                while d_ret is None and not d_halted:
                    d_halted, d_ret = int_code_computer_d.process_next_instruction()

                int_code_computer_e.add_input(d_ret)

                e_halted, e_ret = int_code_computer_e.process_next_instruction()
                while e_ret is None and not e_halted:
                    e_halted, e_ret = int_code_computer_e.process_next_instruction()

                if e_ret is not None:
                    last_e_ret = e_ret
                int_code_computer_a.add_input(last_e_ret)

            thruster_signals_with_feedback_loop.append(last_e_ret)

        maximum_signal_with_feedback_loop = sorted(thruster_signals_with_feedback_loop, reverse=True)[0]

        print(f'Maximum thruster signal with feedback-loop is: {maximum_signal_with_feedback_loop}')


if __name__ == '__main__':
    run_amplifier_controller_software()
