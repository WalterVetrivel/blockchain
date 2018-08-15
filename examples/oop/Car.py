class Car:
    top_speed = 100
    def drive(self):
        print('I\'m driving but not faster than {}kph'.format(self.top_speed))

car = Car()
car.drive()
