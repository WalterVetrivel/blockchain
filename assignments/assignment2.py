names = ['Walter', 'Gracy', 'Dave', 'Andy', 'Nandhini', 'Subha']

for name in names:
    print('Length of ' + name + ' is ' + str(len(name)))
    if len(name) > 5 and 'n' in name.lower():
        print(name + ' has more than 5 characters and has the letter \'n\'')


while len(names) > 0:
    print('Popped: ' + names.pop())
