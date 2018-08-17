import vehicle


class Bus(vehicle.Vehicle):
    model = 'ABC'  # class attribute

    def __init__(self, starting_top_speed=100):  # constructor
        super().__init__(starting_top_speed)
        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)


bus = Bus()
bus.drive()
bus_1 = Bus(250)
bus_1.drive()
Bus.model = 'DEF'
bus.drive()  # model become DEF as model is a class attribute
bus_1.drive()
Bus.top_speed = 50  # the top speed of bus and car_1 are not changed because they are instance attributes
bus.drive()
bus_1.drive()
print(bus.__dict__)
bus.add_warning('New warning')
print(bus)
print(bus.get_warnings())
bus.add_group(['a', 'b'])
