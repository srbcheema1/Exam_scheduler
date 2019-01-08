from srblib import Tabular
from srblib import debug

from .util import credits_calc

class Teacher:
    def __init__(self,idd,name,rank,dept="",desg="",**kwargs):
        self.idd = idd
        self.name = name
        self.rank = int(rank)
        self.dept = dept
        self.desg = desg
        self.extra = list(kwargs.keys())
        self.__dict__.update(kwargs)
        self._credits = credits_calc(rank)
        self.alloted = {}

    def __str__(self):
        a = [
                ["id",self.idd],
                ["name",self.name],
                ["rank",self.rank],
                ["dept",self.dept],
                ["desg",self.desg],
                ["alloted","\n".join([str((x,self.alloted[x])) for x in self.alloted])],
            ]
        if debug:
            a.append(["credits",self._credits])
        for key in self.extra:
            a.append([key,getattr(self,key)])

        a = Tabular(a)
        return a.__str__()

    def __lt__(self,obj):
        if self._credits == obj._credits:
            return self.rank > obj.rank
        return self._credits < obj._credits

    @staticmethod
    def get_teachers(matrix):
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
        idd = 2
        for row in matrix:
            dept = ""
            desg = ""
            kwargs = dict()
            if(cols >= 3): dept = row[2]
            if(cols >= 4): desg = row[3]
            if(cols > 4):
                i = 4
                while i < cols:
                    kwargs[header[i]] = row[i]
                    i += 1
            temp = Teacher(idd,row[0],row[1],dept,desg,**kwargs)
            ret.append(temp)
            idd += 1

        return ret

