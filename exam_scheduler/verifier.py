import sys
from srblib import Tabular

from .util import Response

class Compiler:
    def safefun(fun):
        def inner(matrix):
            if type(matrix) == str:
                matrix = Compiler._read(matrix)
            if type(matrix) is Response: return matrix
            return fun(matrix)
        return inner

    @staticmethod
    @safefun
    def compile_room_list(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage("Error: Insufficient Data")
            r.addMessage("In room_list : " + str(1) + " :")
            r.addMessage("Too few columns, require at least 2 cols for name and teachers")
            r.addMessage("Found " + str(cols) + " cols")
            r.addMessage("")
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[1])
                if int_val < 0:
                    r.addMessage("Error: Invalid Data")
                    r.addMessage("In room_list : " + str(rownum) + " : " + str(2) + " : ")
                    r.addMessage("Second column should contain non-negative integer value")
                    r.addMessage("Found : '" + str(row[1]) + "'")
                    r.addMessage("")
            except:
                r.addMessage("Error: Invalid Data")
                r.addMessage("In room_list : " + str(rownum) + " : " + str(2) + " :")
                r.addMessage("Second column should contain non-negative integer value")
                r.addMessage("Found : '" + str(row[1]) + "'")
                r.addMessage('\n')


            if row[0] in found:
                r.addMessage("Error: Required Unique Value")
                r.addMessage("In room_list : " + str(rownum) + " : " + str(1) + " :")
                r.addMessage("First column should contain unique value")
                r.addMessage("Found : '" + str(row[0]) + "' multiple times")
                r.addMessage("")

            found.add(row[0])

        return r

    @staticmethod
    @safefun
    def compile_work_ratio(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage("Error: Insufficient Data")
            r.addMessage("In work_ratio : " + str(1) + " :")
            r.addMessage("Too few columns, require at least 2 cols for rank and work_ratio")
            r.addMessage("Found " + str(cols) + " cols")
            r.addMessage("")
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[0])
                if int_val < 0:
                    r.addMessage("Error: Invalid Data")
                    r.addMessage("In work_ratio : " + str(rownum) + " : " + str(1) + " :")
                    r.addMessage("First(rank) column should contain non-negative integer value")
                    r.addMessage("Found : '" + str(row[0]) + "'")
                    r.addMessage("")
            except:
                r.addMessage("Error: Invalid Data")
                r.addMessage("In work_ratio : " + str(rownum) + " : " + str(1) + " :")
                r.addMessage("First(rank) column should contain non-negative integer value")
                r.addMessage("Found : '" + str(row[0]) + "'")
                r.addMessage("")


            try:
                int_val = float(row[1])
                if int_val < 0:
                    r.addMessage("Error: Invalid Data")
                    r.addMessage("In work_ratio : " + str(rownum) + " : " + str(2) + " :")
                    r.addMessage("Second(ratio) column should contain non-negative float value")
                    r.addMessage("Found : '" + str(row[1]) + "'")
                    r.addMessage("")
            except:
                r.addMessage("Error: Invalid Data")
                r.addMessage("In work_ratio : " + str(rownum) + " : " + str(2) + " :")
                r.addMessage("Second(ratio) column should contain non-negative float value")
                r.addMessage("Found : '" + str(row[1]) + "'")
                r.addMessage("")


            if row[0] in found:
                r.addMessage("Error: Required Unique Value")
                r.addMessage("In work_ratio : " + str(rownum) + " : " + str(1) + " :")
                r.addMessage("First column should contain unique value")
                r.addMessage("Found : '" + str(row[0]) + "' multiple times")
                r.addMessage("")

            found.add(row[0])

        return r


    @staticmethod
    @safefun
    def compile_teachers_list(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage("Error: Insufficient Data")
            r.addMessage("In teachers_list : " + str(1) + " :")
            r.addMessage("Too few columns, require at least 2 columns for name and rank")
            r.addMessage("Found " + str(cols) + " cols")
            r.addMessage("")
            return r

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            try:
                int_val = int(row[1])
                if int_val < 0:
                    r.addMessage("Error: Invalid Data")
                    r.addMessage("In teachers_list : " + str(rownum) + " : " + str(2) + " :")
                    r.addMessage("Second(rank) column should contain non-negative integer value")
                    r.addMessage("Found : '" + str(row[1]) + "'")
                    r.addMessage("")
            except:
                r.addMessage("Error: Invalid Data")
                r.addMessage("In teachers_list : " + str(rownum) + " : " + str(2) + " :")
                r.addMessage("Second(rank) column should contain non-negative integer value")
                r.addMessage("Found : '" + str(row[1]) + "'")
                r.addMessage("")


            if row[0] in found:
                r.addMessage("Error: Required Unique Value")
                r.addMessage("In teachers_list : " + str(rownum) + " : " + str(1) + " :")
                r.addMessage("First(name) column should contain unique value")
                r.addMessage("Found : '" + str(row[0]) + "' multiple times")
                r.addMessage("")

            found.add(row[0])
        return r


    @staticmethod
    @safefun
    def compile_schedule_list(matrix):
        r = Response()
        header = matrix[0]
        cols = len(header)

        if(cols < 2):
            r.addMessage("Error: Insufficient Data")
            r.addMessage("In schedule_list : " + str(1) + " : ")
            r.addMessage("Too few columns, require at least 2 columns for session_name and rooms")
            r.addMessage("Found " + str(cols) + " cols")
            r.addMessage("")
            return r

        found = set()
        colnum = 0
        for head in header:
            colnum+=1
            if head in found:
                r.addMessage("Error: Invalid Data")
                r.addMessage("In schedule_list : " + str(1) + " : " + str(colnum) + " :")
                r.addMessage("Room names should be unique")
                r.addMessage("Found : '" + str(head) + "' multiple times")
                r.addMessage("")
            found.add(head)

        found = set()
        rownum = 1
        for row in matrix[1:]:
            rownum += 1
            if row[0] in found:
                r.addMessage("Error: Required Unique Value")
                r.addMessage("In schedule_list : " + str(rownum) + " : " + str(1) + " :")
                r.addMessage("First(session_name) column should have unique value")
                r.addMessage("Found : '" + str(row[0]) + "' multiple times")
                r.addMessage("")

            colnum = 1
            for cell in row[1:]:
                colnum+=1
                if cell and cell not in ('Y','y','N','n'):
                    r.addMessage("Error: Invalid Data")
                    r.addMessage("In schedule_list : " + str(rownum) + " : " + str(colnum) + " :")
                    r.addMessage("Cell(other than session-name) can be blank, Y, y, N or n only")
                    r.addMessage("Found : '" + str(row[0]) + "'")
                    r.addMessage("")

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
                r.addMessage("Error: Insufficient Data")
                r.addMessage("'" + str(rank) + "' not present in work_ratio file, (present in teachers_list)")
                r.addMessage("")

        rooms = set()
        for room in room_list[1:]: rooms.add(str(room[0]))
        for room in schedule_list[0][1:]:
            if room not in rooms:
                r.addMessage("Error: Insufficient Data")
                r.addMessage("'" + str(room) + "' not present in room_list file, (present in schedule_list)")
                r.addMessage("")

        return r

    @staticmethod
    def _read(file_path):
        try:
            matrix = Tabular()
            matrix.load_xls(file_path,strict=True)
            return matrix.matrix
        except Exception as e:
            r = Response(e)
            r.addMessage("[Exception] Unable to load file")
            r.addMessage("")
            return r



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
