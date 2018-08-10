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
