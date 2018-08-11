name = 'Walter'
age = 24
message = 'Jesus Christ is Lord'

# format function - the indexes are optional and useful when reusing same variable in the string
print('Hi. My name is {}. I am {} years old. I\'d like t tell you that {}.'.format(name, age, message))
print('Hi. My name is {0}. I am {1} years old. I\'d like t tell you that {2}.'.format(name, age, message))
print('Hi. My name is {name}. I am {age} years old. I\'d like t tell you that {message}.'
      .format(name=name, age=age, message=message))

# python 3 syntax to directly use variables
print(f'Hello again. I\'m {name}. My age is {age}. My message to you is {message}. Thank you.')

amount = 100.59875

print('Amount is: {:6.2f}'.format(amount))
print(f'Amount is : {amount:6.2f}')
