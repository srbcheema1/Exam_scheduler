import os
import sys

from srblib import abs_path
from srblib import Colour
from srblib import SrbJson
from srblib import Tabular
from srblib import debug

from .configurations import config_json
from .configurations import default_output_xlsx_path
from .priority_queue import PriorityQueue
from .session import Session
from .teacher import Teacher
from .util import credits_calc
from .util import randomize

class Scheduler:
    def __init__(self,room_list=None,teachers_list=None,schedule_list=None):
        self.room_list = Scheduler._verified_file(room_list)
        self.teachers_list = Scheduler._verified_file(teachers_list)
        self.schedule_list = Scheduler._verified_file(schedule_list)
        self._configure_paths()

    def _configure_paths(self):
        def configure_path(var_name):
            if not getattr(self,var_name):
                if not config_json[var_name]:
                    path = input('Please provide ' + var_name + ' file : ')
                    path = Scheduler._verified_file(path)
                    config_json[var_name] = path
                    setattr(self,var_name,config_json[var_name])
                else:
                    setattr(self,var_name,config_json[var_name])
            else:
                config_json[var_name] = getattr(self,var_name)
        var_list = ['room_list','teachers_list','schedule_list']
        for var_name in var_list:
            configure_path(var_name)
            Colour.print('Using ' + var_name + ' : ' + Colour.END + getattr(self,var_name), Colour.GREEN)


    def schedule(self,output_path=default_output_xlsx_path,reserved=0):
        teachers_list = Teacher.get_teachers(self.teachers_list)
        session_list = Session.get_sessions(self.schedule_list,self.room_list)

        # for scheduling reserved using -r option
        self.schedule_reserved(teachers_list,session_list,reserved)

        # fake run
        self.generate_duties(teachers_list,session_list)

        # round_n_robin algorithm
        self.round_n_robin(teachers_list,session_list)

        # finished processing ... finally create output
        self.dump_output(teachers_list,session_list,output_path)


    @staticmethod
    def _get_max_rank(teachers_list):
        max_rank = 0
        for teacher in teachers_list:
            max_rank = max(max_rank,teacher.rank)
        return max_rank


    def round_n_robin(self,teachers_list,session_list):
        '''
        Srb's round-n-robin algorithm
        '''
        sorted_teachers_list = teachers_list[:]
        sorted_teachers_list.sort(key=lambda x: int(x.rank))
        session_pq = PriorityQueue(randomize(session_list),key=lambda x: -int(x.unfilled))
        for teacher in sorted_teachers_list:
            done_list = []
            for _ in range(teacher.duties):
                session = session_pq.pop()
                done_list.append(session)
                try: room = session.room_pq.pop()
                except:
                    print('Session broke')
                    print(session)
                    sys.exit(1)
                room.teachers_alloted.append(teacher)
                teacher.alloted[session.name] = room.name
                session.unfilled -= 1
                if room.teachers - len(room.teachers_alloted) > 0: session.room_pq.push(room)
            for session in done_list:
                if session.unfilled > 0: session_pq.push(session)


    def dump_output(self,teachers_list,session_list,output_path):
        matrix = [["Name of Faculty Member","Info"]]
        if debug: matrix[0].extend(['rank','total','res','credits']) # srbdebug
        for session in session_list:
            matrix[0].append(session.name)
        matrix[0].append("Total")

        for teacher in teachers_list:
            if teacher.duties != len(teacher.alloted):
                print('broke on')
                print(teacher)
                sys.exit(1)
            teachers_row = [teacher.name,teacher.info]
            if debug:
                teachers_row.extend([
                    teacher.rank,
                    len(teacher.alloted),
                    len(teacher.alloted_res),
                    int(teacher._credits)
                ])
            for session in session_list:
                if session.name in teacher.alloted: teachers_row.append(teacher.alloted[session.name])
                else: teachers_row.append('-')
            teachers_row.append(len(teacher.alloted))
            matrix.append(teachers_row)

        sheet = Tabular(matrix)
        sheet.write_xls(output_path)


    def generate_duties(self,teachers_list,session_list):
        '''
        Fake run: just to determine teacher duties number
        '''
        teachers_pq = PriorityQueue(randomize(teachers_list),key=lambda x: float(x._credits))
        for session in session_list:
            done_list = []
            for room in session.room_list:
                for _ in range(room.teachers):
                    teacher = teachers_pq.pop()
                    while session.name in teacher.alloted_res: # teacher should not get sametime res and room
                        done_list.append(teacher)
                        teacher = teachers_pq.pop()
                    teacher._credits += credits_calc(teacher.rank)
                    teacher.duties += 1
                    done_list.append(teacher)
            for teacher in done_list:
                teachers_pq.push(teacher)


    def schedule_reserved(self,teachers_list,session_list,reserved):
        '''
        this res is triggered using -r, it will be alloted according to rank
        smaller ranks will get more chances to be reserved
        there is another way, that is using creating a RES room in roomlist
        both differ by name Res for this one RES for that one
        '''
        teachers_list_res = Teacher.get_teachers(self.teachers_list) # create totally new one
        for i in range(len(teachers_list_res)):
            teachers_list_res[i]._credits = 99999 if teachers_list_res[i].rank == 0 else teachers_list_res[i].rank
        teachers_reserved_pq = PriorityQueue(randomize(teachers_list_res),key=lambda x: float(x._credits))
        max_rank = Scheduler._get_max_rank(teachers_list)
        for session in session_list: # reserve
            done_list = []
            for j in range(reserved):
                teacher = teachers_reserved_pq.pop()
                teacher._credits += credits_calc(max_rank-teacher.rank + 1)
                done_list.append(teacher)
                teachers_list[teacher.idd-2].alloted[session.name] = 'Res'
                teachers_list[teacher.idd-2].alloted_res.add(session.name)
                teachers_list[teacher.idd-2]._credits += credits_calc(teacher.rank)
            for teacher in done_list:
                teachers_reserved_pq.push(teacher)


    @staticmethod
    def _verified_file(file_path):
        if not file_path:
            return None
        file_path = abs_path(file_path)
        if not os.path.isfile(file_path):
            Colour.print('No such file : ' + Colour.END + file_path,Colour.RED)
            sys.exit()
        return file_path

