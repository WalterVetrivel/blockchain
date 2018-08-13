import datetime
from random import random, randrange

print('Random number between 0 and 1: ' + str(random()))
print('Random number between 1 and 10 (excluding 10):' + randrange(1, 10))

month = randrange(1, 13)
year = randrange(1900, 2018)

if month in [1, 3, 5, 7, 8, 10, 12]:
    day = randrange(1, 32)
elif month in [4, 6, 9, 11]:
    day = randrange(1, 31)
elif month == 2 and year % 4 == 0:
    day = randrange(1, 30)
elif month == 2 and year % 4 != 0:
    day = randrange(1, 29)

print(datetime.date(day=day, month=month, year=year).strftime('%d-%m-%Y'))
