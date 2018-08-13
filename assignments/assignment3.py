# List of person dictionaries
persons = [
    {
        'name': 'John',
        'age': 24,
        'hobbies': ['Table Tennis', 'Chess']
    },
    {
        'name': 'Jane',
        'age': 22,
        'hobbies': ['Singing', 'Dancing']
    }
]

# Using list comprehension to create a new list containing only the person names
person_names = [person['name'] for person in persons]

print('Person names: ' + str(person_names))

# Using list comprehension to check if all persons are older than 20
if all([person['age'] > 20 for person in persons]):
    print('All persons are older than 20.')
else:
    print('Some persons are younger than 20.')

# Copying persons list to new_persons list - shallow copy
new_persons = persons[:]

# Creating copies of each element - deep copy
for index, person in enumerate(new_persons):
    new_person = {}
    for key, value in person.items():
        new_person[key] = value
    new_persons[index] = new_person
print(new_persons)

# Simpler way to create deep copy
copied_persons = [person.copy() for person in persons]
print(copied_persons)
copied_persons[0]['name'] = 'Dave'
print(copied_persons)
print(persons)

# Modifying name of first element of new_persons list (persons list is not affected because of deep copy)
new_persons[0]['name'] = 'Max'
print(new_persons)
# Printing original persons list to check if it changes
print(persons)

# Unpacking the list into variables
person_1, person_2 = persons

print('Person 1: ' + str(person_1))
print('Person 2: ' + str(person_2))
