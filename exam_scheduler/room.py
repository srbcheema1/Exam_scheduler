from srblib import Tabular

import copy

from .util import credits_calc

class Room:
    def __init__(self,name,teachers,capacity=0,**kwargs):
        '''
        format:
            required positional params:
                name - name of room
                teachers - number of teachers
            optional parameters:
                capacity - capacity of students (default)
            extra:
                kwargs - may include any property
        '''
        self.name = name
        self.teachers = int(teachers)
        self.capacity = int(capacity)
        self.extra = list(kwargs.keys())
        self.__dict__.update(kwargs)
        self.teachers_alloted = []

    def __lt__(self,obj):
        return self.teachers - len(self.teachers_alloted) > obj.teachers - len(obj.teachers_alloted)

    def copy(self):
        ret = copy.deepcopy(self)
        return ret

    def __str__(self):
        a = [
                ["name",self.name],
                ["teachers-required",self.teachers],
                ["capacity",self.capacity],
                ["teachers-alloted"," ".join([teacher.name for teacher in self.teachers_alloted])]
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
            temp = Tabular()
            temp.load_xls(matrix,strict=True)
            matrix = temp
        ret = []
        header = matrix[0]
        cols = len(header)
        if(cols < 2):
            raise Exception('too few columns')

        matrix = matrix[1:]
        for row in matrix:
            capacity = 0
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
