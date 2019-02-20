import sys
from srblib import Tabular

class Verifier:
    @staticmethod
    def _read(file_path):
        matrix = Tabular()
        try:
            matrix.load_xls(file_path,strict=True)
        except:
            print('unable to read file : ',file_path)
            raise
            sys.exit(1)
        return matrix

    @staticmethod
    def verify_room_list(file_path):
        matrix = Verifier._read(file_path)

        header = matrix[0]
        cols = len(header)
        if(cols < 2):
            print('too few columns, require at least 2 columns for name and teachers')
            sys.exit(1)

        found = set()
        for row in matrix[1:]:
            try:
                int_val = int(row[1])
            except:
                print('second column should contain non-negative integer value')
                print(row)
                sys.exit(1)

            if int_val < 0:
                print('second column should contain non-negative integer value')
                print(row)
                sys.exit(1)

            if row[0] in found:
                print('name column should contain unique values')
                print(row)
                sys.exit(1)

            found.add(row[0])


    @staticmethod
    def verify_teachers_list(file_path):
        matrix = Verifier._read(file_path)

        header = matrix[0]
        cols = len(header)
        if(cols < 2):
            print('too few columns, require at least 2 columns for name and rank')
            sys.exit(1)

        found = set()
        for row in matrix[1:]:
            try:
                int_val = int(row[1])
            except:
                print('second column should contain non-negative integer value')
                print(row)
                sys.exit(1)

            if int_val < 0:
                print('second column should contain non-negative integer value')
                print(row)
                sys.exit(1)

            if row[0] in found:
                print('name column should contain unique values')
                print(row)
                sys.exit(1)

            found.add(row[0])


    @staticmethod
    def verify_schedule_list(file_path):
        matrix = Verifier._read(file_path)

        header = matrix[0]
        cols = len(header)
        if(cols < 2):
            print('too few columns, require at least 2 columns for name and room')
            sys.exit(1)

        found = set()
        for head in header:
            if head in found:
                print('room names should be unique, repetition in : ', str(head))
                sys.exit(1)
            found.add(head)

        found = set()
        for row in matrix[1:]:
            if row[0] in found:
                print('name column should contain unique values')
                print(row)
                sys.exit(1)

            for cell in row[1:]:
                if cell and cell not in ('Y','y'):
                    print('cell(other than session-name) can be blank, Y or y only')
                    print(row)
                    sys.exit(1)

            found.add(row[0])


