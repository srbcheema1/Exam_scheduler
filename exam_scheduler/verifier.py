import sys
from srblib import Tabular

class Compiler:
    def safefun(fun):
        def inner(matrix):
            if type(matrix) == str:
                matrix = Compiler._read(matrix)
            if not matrix: return matrix
            return fun(matrix)
        return inner

    @staticmethod
    @safefun
    def compile_room_list(matrix):
        r = Compiler.Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In row : 1')
            r.addMessage("too few columns, require at least 2 cols for name and teachers, found " + str(cols) + " cols")
            r.addMessage(str(header))
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[1])
            except:
                r.addMessage('In row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')

            if int_val < 0:
                r.addMessage('In row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')

            if row[0] in found:
                r.addMessage('In row : ' + str(rownum) + ' column : 1 found : ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first column should contain unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            found.add(row[0])

        return r


    @staticmethod
    @safefun
    def compile_teachers_list(matrix):
        r = Compiler.Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In row : 1')
            r.addMessage(str(header))
            r.addMessage("too few columns, require at least 2 columns for name and rank, found " + str(cols) + "cols")
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[1])
            except:
                r.addMessage('In row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')

            if int_val < 0:
                r.addMessage('In row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')

            if row[0] in found:
                r.addMessage('In row : ' + str(rownum) + ' column : 1 found : ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first column should contain unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            found.add(row[0])
        return r


    @staticmethod
    @safefun
    def compile_schedule_list(matrix):
        r = Compiler.Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In row : 1')
            r.addMessage(str(header))
            r.addMessage("too few columns, require at least 2 columns for name and rank, found " + str(cols) + "cols")
            return r

        found = set()
        colnum = 0
        for head in header:
            colnum+=1
            if head in found:
                r.addMessage('In row : ' + str(1) + ' column : ' + str(colnum) + ' found : ' + head)
                r.addMessage(str(header))
                r.addMessage("room names should have unique value, found '" + str(head) + "' twice")
                r.addMessage('\n')
            found.add(head)

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            if row[0] in found:
                r.addMessage('In row : ' + str(rownum) + ' column : 1' + ' found ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first(name) column should have unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            colnum = 1
            for cell in row[1:]:
                colnum+=1
                if cell and cell not in ('Y','y','N','n'):
                    r.addMessage('In row : ' + str(rownum) + ' column : ' + str(colnum) + ' found : ' + str(cell))
                    r.addMessage(str(row))
                    r.addMessage('cell(other than session-name) can be blank, Y, y, N or n only')
                    r.addMessage('\n')

            found.add(row[0])
        return r

    class Response:
        def __init__(self,execption=None):
            self.__message = []
            self.exception = execption

        def addMessage(self, msg):
            self.__message.append(msg)
            return self

        def __str__(self):
            return '\n'.join(self.__message)

        def __bool__(self):
            return len(self.__message)==0 and not self.exception

        def safe(self):
            if self.exception:
                raise self.exception
            return bool(self)

        def json(self):
            return {
                'message':str(self),
                'status':bool(self)
            }




    @staticmethod
    def _read(file_path):
        matrix = Tabular()
        try:
            matrix.load_xls(file_path,strict=True)
        except BaseException as e:
            res = Compiler.Response(e)
            res.addMessage('unable to load file ' + file_path)
        return matrix



class Verifier:
    '''
    this class is for commandline purpose, should not be used as part of module
    '''
    def dieifbad(fun):
        def inner(*args,**kwargs):
            ret = fun(*args,**kwargs)
            if not ret.safe():
                print(ret)
                sys.exit(1)
        return inner

    @staticmethod
    @dieifbad
    def verify_room_list(file_path):
        return Compiler.compile_room_list(file_path)

    @staticmethod
    @dieifbad
    def verify_teachers_list(file_path):
        return Compiler.compile_teachers_list(file_path)

    @staticmethod
    @dieifbad
    def verify_schedule_list(file_path):
        return Compiler.compile_schedule_list(file_path)
