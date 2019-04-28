import sys
from srblib import Tabular

from .util import Response

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
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In room_list, row : 1')
            r.addMessage("too few columns, require at least 2 cols for name and teachers, found " + str(cols) + " cols")
            r.addMessage(str(header))
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[1])
                if int_val < 0:
                    r.addMessage('In room_list, row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                    r.addMessage(str(row))
                    r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                    r.addMessage('\n')
            except:
                r.addMessage('In room_list, row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')


            if row[0] in found:
                r.addMessage('In room_list, row : ' + str(rownum) + ' column : 1 found : ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first column should contain unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            found.add(row[0])

        return r

    @staticmethod
    @safefun
    def compile_work_ratio(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In work_ratio, row : 1')
            r.addMessage("too few columns, require at least 2 cols for rank and work_ratio, found " + str(cols) + " cols")
            r.addMessage(str(header))
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[0])
                if int_val < 0:
                    r.addMessage('In work_ratio, row : ' + str(rownum) + ' column : 1 found : ' + str(row[1]))
                    r.addMessage(str(row))
                    r.addMessage("first(rank) column should contain non-negative integer value, found '" + str(row[1]) + "'")
                    r.addMessage('\n')
            except:
                r.addMessage('In work_ratio, row : ' + str(rownum) + ' column : 1 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("first(rank) column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')


            try:
                int_val = float(row[1])
                if int_val < 0:
                    r.addMessage('In work_ratio, row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                    r.addMessage(str(row))
                    r.addMessage("second column should contain non-negative float value, found '" + str(row[1]) + "'")
                    r.addMessage('\n')
            except:
                r.addMessage('In work_ratio, row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative float value, found '" + str(row[1]) + "'")
                r.addMessage('\n')


            if row[0] in found:
                r.addMessage('In work_ratio, row : ' + str(rownum) + ' column : 1 found : ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first column should contain unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            found.add(row[0])

        return r


    @staticmethod
    @safefun
    def compile_teachers_list(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In teachers_list, row : 1')
            r.addMessage(str(header))
            r.addMessage("too few columns, require at least 2 columns for name and rank, found " + str(cols) + "cols")
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[1])
                if int_val < 0:
                    r.addMessage('In teachers_list, row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                    r.addMessage(str(row))
                    r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                    r.addMessage('\n')
            except:
                r.addMessage('In teachers_list, row : ' + str(rownum) + ' column : 2 found : ' + str(row[1]))
                r.addMessage(str(row))
                r.addMessage("second column should contain non-negative integer value, found '" + str(row[1]) + "'")
                r.addMessage('\n')


            if row[0] in found:
                r.addMessage('In teachers_list, row : ' + str(rownum) + ' column : 1 found : ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first column should contain unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            found.add(row[0])
        return r


    @staticmethod
    @safefun
    def compile_schedule_list(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage('In schedule_list, row : 1')
            r.addMessage(str(header))
            r.addMessage("too few columns, require at least 2 columns for name and rank, found " + str(cols) + "cols")
            return r

        found = set()
        colnum = 0
        for head in header:
            colnum+=1
            if head in found:
                r.addMessage('In schedule_list, row : ' + str(1) + ' column : ' + str(colnum) + ' found : ' + head)
                r.addMessage(str(header))
                r.addMessage("room names should have unique value, found '" + str(head) + "' twice")
                r.addMessage('\n')
            found.add(head)

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            if row[0] in found:
                r.addMessage('In schedule_list, row : ' + str(rownum) + ' column : 1' + ' found ' + str(row[0]))
                r.addMessage(str(row))
                r.addMessage("first(name) column should have unique value, found '" + str(row[0]) + "' twice")
                r.addMessage('\n')

            colnum = 1
            for cell in row[1:]:
                colnum+=1
                if cell and cell not in ('Y','y','N','n'):
                    r.addMessage('In schedule_list, row : '
                            + str(rownum) + ' column : ' + str(colnum) + ' found : ' + str(cell))
                    r.addMessage(str(row))
                    r.addMessage('cell(other than session-name) can be blank, Y, y, N or n only')
                    r.addMessage('\n')

            found.add(row[0])
        return r


    @staticmethod
    def crosscompile(teachers_list,room_list,schedule_list,work_ratio):
        '''
        only to be called after compilation is done(all files are OK)
        '''
        teachers_list = Compiler._read(teachers_list)
        work_ratio = Compiler._read(work_ratio)
        room_list = Compiler._read(room_list)
        schedule_list = Compiler._read(schedule_list)

        r = Response()

        ratio_rank = set()
        for row in work_ratio[1:]: ratio_rank.add(int(row[0]))
        rank_list = set()
        for row in teachers_list[1:]: rank_list.add(int(row[1]))
        for rank in rank_list:
            if rank == 0: continue
            if rank not in ratio_rank:
                r.addMessage(str(rank) + ' not present in work_ratio file, (present in teachers_list)')
                r.addMessage('\n')

        rooms = set()
        for room in room_list[1:]: rooms.add(str(room[0]))
        for room in schedule_list[0][1:]:
            if room not in rooms:
                r.addMessage(str(room) + ' not present in room_list file, (present in schedule_list)')
                r.addMessage('\n')

        return r

    @staticmethod
    def _read(file_path):
        matrix = Tabular()
        try:
            matrix.load_xls(file_path,strict=True)
        except BaseException as e:
            res = Response(e)
            res.addMessage('unable to load file ' + file_path)
        return matrix.matrix



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

    @staticmethod
    @dieifbad
    def verify_work_ratio(file_path):
        return Compiler.compile_work_ratio(file_path)

    @staticmethod
    @dieifbad
    def crossverify(teachers_list,room_list,schedule_list,work_ratio):
        return Compiler.crosscompile(teachers_list,room_list,schedule_list,work_ratio)
