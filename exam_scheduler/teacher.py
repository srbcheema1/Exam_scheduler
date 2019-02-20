from srblib import Tabular
from srblib import debug

from .util import credits_calc

class Teacher:
    def __init__(self,idd,name,rank,info="",**kwargs):

        '''
        format:
            required positional params:
                idd - unique id (ususlly not by user)
                name - name of teacher
                rank - rank of teacher
            optional parameters:
                info - any extra info
            extra:
                kwargs - may include any property
        '''
        self.idd = idd
        self.name = name
        self.rank = int(rank)
        self.info = info
        self.subclass = "" # extract out if something after name in brackets
        self.info = info
        self.extra = list(kwargs.keys())
        self.__dict__.update(kwargs)
        self._credits = credits_calc(rank)
        self.alloted = {}
        self.alloted_res = set()
        self.duties = 0

    def __str__(self):
        a = [
                ["id",self.idd],
                ["name",self.name],
                ["rank",self.rank],
                ["info",self.info],
                ["duties",self.duties],
                ["alloted_res","\n".join([str(x) for x in self.alloted_res])],
                ["alloted","\n".join([str((x,self.alloted[x])) for x in self.alloted])],
            ]
        if debug: a.append(["credits",self._credits])
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
            temp = Tabular()
            temp.load_xls(matrix,strict=True)
            matrix = temp
        ret = []
        header = matrix[0]
        cols = len(header)
        if(cols < 2):
                raise Exception('too few columns')
        matrix = matrix[1:]
        idd = 2
        for row in matrix:
            info = ""
            kwargs = dict()
            if(cols >= 3): info = row[2]
            if(cols > 3):
                i = 3
                while i < cols:
                    kwargs[header[i]] = row[i]
                    i += 1
            temp = Teacher(idd,row[0],row[1],info,**kwargs)
            ret.append(temp)
            idd += 1

        return ret

