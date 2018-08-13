simple_list = [1, 2, 3, 4, 5]


def double_number(el):
    return el * 2


# map function returns a map object that can be converted to a list
doubled_list = list(map(double_number, simple_list))
print(doubled_list)

string_list = list(map(str, simple_list))
print(string_list)

# using lambda functions
lambda_list = list(map(lambda el: el * 3, simple_list))
print(lambda_list)
