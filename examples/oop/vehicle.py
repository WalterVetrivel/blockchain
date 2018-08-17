class Vehicle:
    def __init__(self, starting_top_speed=100):  # constructor
        self.top_speed = starting_top_speed  # instance attribute
        self.__warnings = []  # __ signifies private access modifier

    def __repr__(self):
        print('Printing...')
        return 'Top speed: {}, Warnings: {}'.format(self.top_speed, len(self.__warnings))

    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings

    def drive(self):
        print('I\'m driving a {} but not faster than {}kph'.format(self.model, self.top_speed))