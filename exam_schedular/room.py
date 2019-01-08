
from srblib import Tabular
from util import credits_calc

class Room:
    def __init__(self,name,teachers,capacity=0,**kwargs):
        self.name = name
        self.teachers = teachers
        self.capacity = capacity
        self.extra = list(kwargs.keys())
        self.__dict__.update(kwargs)

    def __str__(self):
        a = [
                ["name",self.name],
                ["teachers",self.teachers],
                ["capacity",self.capacity],
            ]
        for key in self.extra:
            a.append([key,getattr(self,key)])

        a = Tabular(a)
        return a.__str__()

    @staticmethod
    def get_rooms(matrix):
        '''
        input should be a Tabular object, or a path
        '''
        if type(matrix) is str:
            matrix = Tabular(matrix)
        ret = []
        header = matrix[0]
        cols = len(header)
        if(cols < 2):
                raise Exception('too few columns')
        matrix = matrix[1:]
        for row in matrix:
            capacity = ""
            kwargs = dict()
            if(cols >= 3): capacity = row[2]
            if(cols > 3):
                i = 3
                while i < cols:
                    kwargs[header[i]] = row[i]
                    i += 1
            temp = Room(row[0],row[1],capacity,**kwargs)
            ret.append(temp)

        return ret

