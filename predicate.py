class Predicate:

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return 'predicate: ' + self.name + \
        '\n  arguments: ' + str(self.arguments)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
