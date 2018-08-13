simple_list = [1, 2, 3, 4]
simple_list.extend([5, 6, 7])
print(simple_list)

d = {'name': 'Walter', 'age': 24}
print(d.items())

for k, v in d.items():
    print(k, v)

t = (1, 2, 3)
print(t.index(2))

s = {'Walter', 'Gracy', 'Dave', 'Nandhu'}
s_friends = {'Dave', 'Nandhu', 'Aisha'}

print(s.intersection(s_friends))
print(s.union(s_friends))

list_1 = [1, 2, 3, -5]
if all([el > 0 for el in list_1]):
    print('All elements are greater than 0')
elif any([el > 0 for el in list_1]):
    print('One or more elements are greater than 0')
else:
    print('No element is greater than 0')


def unlimited_arguments(*args):
    print(args)
    for arg in args:
        print(arg)


unlimited_arguments(1, 2, 3, 4, 5)
unlimited_arguments(*['a', 'b', 'c'])  # * unpacks list to comma separated arguments


def keyword_arguments(**keyword_args):  # ** converts named parameters to dictionary
    print(keyword_args)
    for argument in keyword_args:
        print(argument)
    for key, value in keyword_args.items():
        print(key + ':' + str(value))


keyword_arguments(name='Walter', age=24)
# keyword_arguments('a', 'b') This results in an error. If ** is used, named arguments must be specified
