# This file is part of IPPDDL Parser, available at <https://github.com/AndreMoukarzel/ippddl-parser/>.

class Predicate:

    def __init__(self, name: str, arguments: dict):
        self.name = name
        self.arguments = tuple(arguments)  # Make parameters a tuple so we can hash this if need be
        self.objects = frozenset([key for key in arguments.keys()])
        self.object_types = [val for val in arguments.values()]


    def __str__(self):
        return 'Predicate: ' + self.name + \
                '\n  objects: ' + str([i for i in self.objects]) + \
                '\n  object_types: ' + str([i for i in self.object_types]) + '\n'


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


if __name__ == '__main__':
    pred = Predicate('at', {'?ag': 'agent', '?x': 'location'})
    print(pred)
    pred = Predicate('on', {'?x': 'block', '?y': 'block'})
    print(pred)
