import sys

from srblib import Colour
from srblib import Tabular

from .room import Room

class Session:
    def __init__(self,name,room_list):
        self.name = name
        self.room_list = room_list

    def __str__(self):
        a = [[self.name]]
        for room in self.room_list:
            a[0].append(room.name)
        a = Tabular(a)
        return a.__str__()

    @staticmethod
    def get_sessions(matrix,room_data):
        '''
        input matrix should be a Tabular object, or a path
        room_data should be a tabular object or a path
        '''
        if type(matrix) is str:
            matrix = Tabular(matrix)
        if type(room_data) is str:
            room_data = Room.get_rooms(room_data)

        room_json = {}
        for room in room_data:
            room_json[room.name] = room

        ret = []
        header = matrix[0][1:] # remove first elem from header
        cols = len(header) + 1
        if(cols < 2):
                raise Exception('too few columns')
        for i in range(1,len(matrix)):
            row = matrix[i]
            room_list = []
            for room in header:
                need = row[room]
                if need == 'y' or need == 'Y':
                    if room in room_json:
                        room_list.append(room_json[room])
                    else:
                        # raise Exception('Room ' +room+ ' not present in rooms file')
                        Colour.print('Room ' + room + ' not present in room list',Colour.RED)
                        sys.exit()

            temp = Session(row[0], room_list)
            ret.append(temp)

        return ret
