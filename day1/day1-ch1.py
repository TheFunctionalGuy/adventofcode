import math


# Solution for: https://adventofcode.com/2019/day/1
def calculate_fuel_requirement(mass: int) -> int:
    return math.floor(mass / 3) - 2


def test_fuel_calculation():
    for mass in {12: 2, 14: 2, 1969: 654, 100756: 33583}.items():
        if mass[1] == calculate_fuel_requirement(mass[0]):
            print(f'Your function yields the expected result for input: {mass[0]}')
        else:
            print(f'Your function does not yield the expected result for input: {mass[0]}')
            return False

    return True


def calculate_fuel_counter():
    with open('input.txt', mode='r') as input_file:
        masses = input_file.readlines()
        masses = map(lambda x: int(x.rstrip()), masses)
        fuel_requirements = map(lambda x: calculate_fuel_requirement(x), masses)
        result = sum(fuel_requirements)

        print(f'The resulting fuel requirement for this input list is: {result}')


def calculate_fuel_requirement_with_additional_fuel(mass: int) -> int:
    fuel = math.floor(mass / 3) - 2

    if fuel > 0:
        return fuel + calculate_fuel_requirement_with_additional_fuel(fuel)
    else:
        return 0


def test_additional_fuel_calculation():
    for mass in {14: 2, 1969: 966, 100756: 50346}.items():
        if mass[1] == calculate_fuel_requirement_with_additional_fuel(mass[0]):
            print(f'Your function yields the expected result for input: {mass[0]}')
        else:
            print(f'Your function does not yield the expected result for input: {mass[0]}')
            return False

    return True


def calculate_fuel_counter_with_additional_fuel():
    with open('input.txt', mode='r') as input_file:
        masses = input_file.readlines()
        masses = map(lambda x: int(x.rstrip()), masses)
        fuel_requirements_with_additional_fuel = map(lambda x: calculate_fuel_requirement_with_additional_fuel(x),
                                                     masses)
        result = sum(fuel_requirements_with_additional_fuel)

        print(f'The resulting fuel requirement (with additional fuel) for this input is: {result}')


if __name__ == '__main__':
    if test_fuel_calculation():
        calculate_fuel_counter()
    if test_additional_fuel_calculation():
        calculate_fuel_counter_with_additional_fuel()
