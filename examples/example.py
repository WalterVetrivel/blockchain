name = input('Please enter your name: ')
print('Opening file')
file = open('name.txt', mode='w')
print('Writing to file')
file.write(name)
print('Closing file')
file.close()
print('Reopening file')
file = open('name.txt', mode='r')
print('Your name is: ' + file.read())
file.close()
