import vehicle


class Car(vehicle.Vehicle):
    model = 'ABC'  # class attribute

    def honk(self):
        print('Honk honk!')


car = Car()
car.drive()
car_1 = Car(250)
car_1.drive()
Car.model = 'DEF'
car.drive()  # model become DEF as model is a class attribute
car_1.drive()
Car.top_speed = 50  # the top speed of car and car_1 are not changed because they are instance attributes
car.drive()
car_1.drive()
print(car.__dict__)
car.add_warning('New warning')
print(car)
print(car.get_warnings())
car.honk()
