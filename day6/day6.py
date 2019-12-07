from typing import Dict

from anytree import Node, PreOrderIter


# Solution for: https://adventofcode.com/2019/day/6
def count_orbits():
    with open('input.txt', mode='r') as input_file:
        # Part one
        lines = [line.rstrip() for line in input_file]
        nodes = {}

        for line in lines:
            orbits = line.split(')')
            # Create new node or get existing node
            if orbits[0] not in nodes:
                node_1 = Node(orbits[0])
                nodes[orbits[0]] = node_1
            else:
                node_1 = nodes[orbits[0]]

            # Create new node or get existing node
            if orbits[1] not in nodes:
                node_2 = Node(orbits[1], parent=node_1)
                nodes[orbits[1]] = node_2
            else:
                nodes[orbits[1]].parent = node_1

        # Traversal tree
        number_of_ancestors = [len(node.ancestors) for node in PreOrderIter(nodes['COM'])]
        number_of_orbits = sum(number_of_ancestors)
        print(f'The total number of orbits is: {number_of_orbits}')

        # Part two
        get_number_of_orbital_transfers_required(nodes)


def get_number_of_orbital_transfers_required(nodes: Dict[str, Node]):
    # Get connection node
    you_path = nodes['YOU'].path
    santa_path = nodes['SAN'].path
    intersected_path = set(you_path).intersection(set(santa_path))

    # Get path length towards connection node
    path_length = 0

    for node in intersected_path:
        if path_length < len(node.ancestors):
            path_length = len(node.ancestors)

    path_from_connection_node_to_you = list(filter(lambda x: len(x.ancestors) > path_length, you_path))
    path_from_connection_node_to_santa = list(filter(lambda x: len(x.ancestors) > path_length, santa_path))

    print(f'Minimum number of orbital transfers is: '
          f'{len(path_from_connection_node_to_you) + len(path_from_connection_node_to_santa) - 2}')


if __name__ == '__main__':
    count_orbits()
