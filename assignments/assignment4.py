def normal_function(parameter_function, *unlimited_parameters):
    """Accepts one function and unlimited number of other data as parameters and then executes
    the parameter function for every argument that is passed.
    Arguments:
        :parameter_function: A function that is executed for each additional argument passed
        :*unlimited_parameters: Numbers that are passed to the function"""
    for parameter in unlimited_parameters:
        # the parameter function is called for every additional argument
        print('{:^20}'.format(parameter_function(parameter)))


def other_function(argument):
    return argument * 2


normal_function(other_function, 5, 4, 3, 2, 1)
normal_function(lambda el: el * 2, *[1, 2, 3, 4, 5])
