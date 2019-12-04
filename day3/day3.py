from typing import List, Set, Tuple


# Solution for: https://adventofcode.com/2019/day/3
def find_manhattan_distance_of_closest_intersection():
    with open('input.txt', mode='r') as input_file:
        # Part one
        # Get both wires
        wires = [wire.rstrip() for wire in input_file]
        wire_path_1 = wires[0].split(sep=',')
        wire_path_2 = wires[1].split(sep=',')

        wire_positions_1 = trace_wire(wire_path_1)
        wire_positions_2 = trace_wire(wire_path_2)

        intersections = wire_positions_1.intersection(wire_positions_2)
        distances = map(lambda point: abs(point[0]) + abs(point[1]), intersections)
        sorted_distances = sorted(distances)
        closest_intersection = sorted_distances[0]

        print(f'The closest intersection is distance {closest_intersection} away.')

        # Part two
        distance_of_shortest_path_to_intersection = find_shortest_path_to_intersection(wire_path_1, wire_path_2,
                                                                                       intersections)

        print(f'The shortest path to an intersection is {distance_of_shortest_path_to_intersection} long.')


def trace_wire(wire_path: List[str]) -> Set[Tuple[int, int]]:
    wire_positions = set()
    latest_position = (0, 0)

    for instruction in wire_path:
        direction = instruction[0]
        steps = int(instruction[1:])
        if direction == 'R':
            for i in range(1, steps + 1):
                wire_positions.add((latest_position[0] + i, latest_position[1]))
            latest_position = latest_position[0] + steps, latest_position[1]
        elif direction == 'D':
            for i in range(1, steps + 1):
                wire_positions.add((latest_position[0], latest_position[1] - i))
            latest_position = latest_position[0], latest_position[1] - steps
        elif direction == 'L':
            for i in range(1, steps + 1):
                wire_positions.add((latest_position[0] - i, latest_position[1]))
            latest_position = latest_position[0] - steps, latest_position[1]
        else:
            for i in range(1, steps + 1):
                wire_positions.add((latest_position[0], latest_position[1] + i))
            latest_position = latest_position[0], latest_position[1] + steps

    return wire_positions


def find_shortest_path_to_intersection(wire_path_1: List[str], wire_path_2: List[str], intersections: Set[Tuple[int, int]]) -> int:
    path_lengths_to_intersection = []

    for intersection in intersections:
        length_path1 = get_path_length_to_intersection(wire_path_1, intersection)
        length_path2 = get_path_length_to_intersection(wire_path_2, intersection)

        path_lengths_to_intersection.append(length_path1 + length_path2)

    sorted_path_lengths = sorted(path_lengths_to_intersection)
    return sorted_path_lengths[0]


def get_path_length_to_intersection(wire_path: List[str], intersection: Tuple[int, int]) -> int:
    path_length = 0
    current_position = (0, 0)
    path_hit_intersection = False

    for instruction in wire_path:
        if path_hit_intersection:
            break

        direction = instruction[0]
        steps = int(instruction[1:])

        if direction == 'R':
            for _ in range(steps):
                current_position = current_position[0] + 1, current_position[1]
                path_length += 1

                if current_position == intersection:
                    path_hit_intersection = True
                    break
        elif direction == 'D':
            for _ in range(steps):
                current_position = current_position[0], current_position[1] - 1
                path_length += 1

                if current_position == intersection:
                    path_hit_intersection = True
                    break
        elif direction == 'L':
            for _ in range(steps):
                current_position = current_position[0] - 1, current_position[1]
                path_length += 1

                if current_position == intersection:
                    path_hit_intersection = True
                    break
        else:
            for _ in range(steps):
                current_position = current_position[0], current_position[1] + 1
                path_length += 1

                if current_position == intersection:
                    path_hit_intersection = True
                    break

    return path_length


if __name__ == '__main__':
    find_manhattan_distance_of_closest_intersection()
