import operator


# Solution for: https://adventofcode.com/2019/day/4
def get_number_of_valid_passwords():
    # Part one
    number_of_valid_passwords = 0

    for password in range(183564, 657474 + 1):
        if password_meets_criteria(str(password), 2, operator.ge):
            number_of_valid_passwords += 1

    print(f'The number of valid passwords is: {number_of_valid_passwords}')

    # Part two
    number_of_valid_passwords_with_additional_criteria = 0

    for password in range(183564, 657474 + 1):
        if password_meets_criteria(str(password), 2, operator.eq):
            number_of_valid_passwords_with_additional_criteria += 1

    print(f'The number of passwords meeting the additional criteria is: '
          f'{number_of_valid_passwords_with_additional_criteria}')


def password_meets_criteria(password: str, group_size: int, group_size_operator: operator) -> bool:
    same_digit_group_sizes = []
    same_digit_group = str(password)[0]

    for i in range(5):
        if int(str(password)[i]) > int(str(password)[i + 1]):
            return False
        if str(password)[i] == str(password)[i + 1]:
            same_digit_group += str(password)[i + 1]
        else:
            same_digit_group_sizes.append(len(same_digit_group))
            same_digit_group = str(password)[i + 1]

    # Append last group also
    same_digit_group_sizes.append(len(same_digit_group))

    group_size_met = [group_size_operator(same_digit_group_size, group_size) for same_digit_group_size in
                      same_digit_group_sizes]

    if True in group_size_met:
        return True


if __name__ == '__main__':
    get_number_of_valid_passwords()
