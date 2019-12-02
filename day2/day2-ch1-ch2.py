import copy
from typing import List


# Solution for: https://adventofcode.com/2019/day/2
def process_int_code():
    with open('input.txt', mode='r') as int_code_file:
        int_codes = [int_codes.rstrip().split(sep=',') for int_codes in int_code_file]
        int_codes = int_codes[0]
        int_codes = [int(int_code) for int_code in int_codes]
        int_codes_backup = copy.deepcopy(int_codes)

        # Part one
        int_codes[1] = 12
        int_codes[2] = 2

        result_part_one = run_int_codes(int_codes)
        print(f'Answer to part one is: {result_part_one}')

        # Part two
        for noun in range(100):
            for verb in range(100):
                run_copy = copy.deepcopy(int_codes_backup)
                run_copy[1] = noun
                run_copy[2] = verb

                if run_int_codes(run_copy) == 19690720:
                    print(f'Answer to part two is: {100 * noun + verb}')


def run_int_codes(int_codes: List[int]) -> int:
    for i in range(len(int_codes) // 4):
        op, arg1, arg2, tar = int_codes[i * 4 + 0], int_codes[i * 4 + 1], int_codes[i * 4 + 2], int_codes[i * 4 + 3]

        if op == 1:
            int_codes[tar] = int_codes[arg1] + int_codes[arg2]
        if op == 2:
            int_codes[tar] = int_codes[arg1] * int_codes[arg2]
        if op == 99:
            break

    return int_codes[0]


if __name__ == '__main__':
    process_int_code()
