name = input('Enter your name: ')
age = input('Enter your age: ')


def concatenate_strings(string_1, string_2):
    print(str(string_1) + ' ' + str(string_2))


def calculate_decades(age):
    decades = int(age / 10)
    return str(decades)


concatenate_strings(name, age)
print('You\'ve lived for: ' + calculate_decades(int(age)) + ' decades.')
