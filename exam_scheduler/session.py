import sys
import re

from srblib import Colour
from srblib import Tabular

from .room import Room
from .priority_queue import PriorityQueue
from .verifier import Verifier


class Session:
    def __init__(self,name,room_list):
        self.name = name
        self.base = Session.get_base(name)
        batch = re.search(r'\((.*?)\)',name).group(1)
        self.batch = batch if batch else ""

        self.room_list = room_list
        self.remaining = 0 # slots not filled
        for room in room_list:
            self.remaining += room.teachers
        self.room_pq = PriorityQueue(self.room_list)

    def __str__(self):
        a = [[self.name]]
        a[0].append('rem ' + str(self.remaining))
        a[0].append('top_pq ' + self.room_pq.top().name)
        a[0].append('top_pq_unfill ' + str(self.room_pq.top().unfilled()))
        a[0].append('top_pq_fill ' + str(self.room_pq.top().filled()))
        a[0].append('top_pq_type ' + self.room_pq.top().get_type())
        b = [[' => ']]
        for room in self.room_list:
            b[0].append(room.name + ' ' + str(room.teachers - len(room.teachers_alloted)))
        a = Tabular(a)
        b = Tabular(b)
        return a.__str__() + '\n' + b.__str__() + '\n'

    def __lt__(self,obj):
        self_top = self.room_pq.top()
        obj_top = obj.room_pq.top()
        if self_top.empty() and not obj_top.empty(): return True # special case, empty room should be filled first
        if self_top.unfilled() == obj_top.unfilled() and self_top.filled() == obj_top.filled():
            if self.remaining == obj.remaining:
                return self_top < obj_top
            else:
                return self.remaining > obj.remaining
        return self_top < obj_top

    @staticmethod
    def get_base(name):
        return re.sub(r'\((.*?)\)','',name)

    @staticmethod
    def get_sessions(matrix,room_data,workratio):
        '''
        input matrix should be a Tabular object, or a path
        room_data should be a tabular object or a path
        workratio is obj of WorkRatio
        '''
        if type(matrix) is str:
            Verifier.verify_schedule_list(matrix)
            temp = Tabular()
            temp.load_xls(matrix,strict=True)
            matrix = temp
        if type(room_data) is str:
            room_data = Room.get_rooms(room_data,workratio)

        room_json = {}
        for room in room_data:
            room_json[room.name] = room

        ret = []
        header = matrix[0][1:] # remove first elem from header
        cols = len(header) + 1
        if(cols < 2):
                raise Exception('too few columns')
        for row in matrix:
            room_list = []
            for room in header:
                need = row[room]
                if need == 'y' or need == 'Y':
                    if room in room_json:
                        room_list.append(room_json[room].copy())
                    else:
                        raise Exception('Room ' +room+ ' not present in rooms file')

            temp = Session(row[0], room_list)
            ret.append(temp)

        return ret
