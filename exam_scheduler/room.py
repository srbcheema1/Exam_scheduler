from srblib import Tabular

import copy

from .verifier import Verifier

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
        self._credits = -1 # weitage of room
        self.workratio = None # WorkRatio object
        self.reserved = False
        if len(str(self.name)) > 2 and str(self.name)[0:3] == 'Res':
            self.reserved = True

    def unfilled(self):
        return self.teachers - len(self.teachers_alloted)

    def filled(self):
        return len(self.teachers_alloted)

    def empty(self):
        if len(self.teachers_alloted) == 0:
            return True
        return False

    def get_credits(self):
        self._credits = 0
        for teacher in self.teachers_alloted:
            self._credits += self.workratio.credits_calc(teacher.rank)
        return self._credits

    def __eq__(self,obj):
        if not self < obj and not obj < self:
            return True
        return False

    def __lt__(self,obj):
        if self.empty() and not obj.empty(): return True # special case when self is empty, it must get high priority
        if self.unfilled() == obj.unfilled():
            if self.filled() == obj.filled():
                return self.get_credits() < obj.get_credits()
            else:
                return self.filled() < obj.filled()
        return self.unfilled() > obj.unfilled()

    def copy(self):
        ret = copy.deepcopy(self)
        return ret

    def get_type(self):
        arr = []
        for teacher in self.teachers_alloted:
            arr.append(teacher.rank)
        arr.sort()
        return arr.__str__()

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
    def get_rooms(matrix,workratio):
        '''
        input should be a Tabular object, or a path
        workratio is object of WorkRatio
        '''
        if type(matrix) is str:
            Verifier.verify_room_list(matrix)
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
            temp.workratio = workratio
            ret.append(temp)

        return ret
