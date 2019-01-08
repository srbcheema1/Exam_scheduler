import os
import sys

from srblib import abs_path
from srblib import Colour
from srblib import SrbJson
from srblib import Tabular

from .configurations import config_json
from .configurations import default_output_xlsx_path
from .priority_queue import PriorityQueue
from .session import Session
from .teacher import Teacher
from .util import credits_calc
from .util import randomize

class Scheduler:
    def __init__(self,room_list=None,teacher_list=None,schedule_list=None):
        self.room_list = Scheduler._verified_file(room_list)
        self.teacher_list = Scheduler._verified_file(teacher_list)
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
        var_list = ['room_list','teacher_list','schedule_list']
        for var_name in var_list:
            configure_path(var_name)
            Colour.print('Using ' + var_name + ' : ' + Colour.END + getattr(self,var_name), Colour.GREEN)

    def schedule(self,output_path=default_output_xlsx_path):
        teacher_list_for_pq = randomize(Teacher.get_teachers(self.teacher_list))
        pq = PriorityQueue(teacher_list_for_pq)

        teacher_list = Teacher.get_teachers(self.teacher_list)
        session_list = Session.get_sessions(self.schedule_list,self.room_list)

        for session in session_list:
            done_list = []
            for i in range(len(session.room_list)):
                for j in range(session.room_list[i].teachers):
                    teacher = pq.pop()
                    session.room_list[i].teachers_alloted.append(teacher)
                    teacher._credits += credits_calc(teacher.rank)
                    done_list.append(teacher)
                    teacher_list[teacher.idd-2].alloted[session.name] = session.room_list[i].name
            for teacher in done_list:
                pq.push(teacher)

        matrix = [["Name of Faculty Member","Designation","Dept"]]
        for session in session_list:
            matrix[0].append(session.name)
        matrix[0].append("Total")

        for teacher in teacher_list:
            teacher_row = [teacher.name,teacher.desg,teacher.dept]
            for session in session_list:
                if session.name in teacher.alloted:
                    teacher_row.append(teacher.alloted[session.name])
                else:
                    teacher_row.append('-')
            teacher_row.append(len(teacher.alloted))
            matrix.append(teacher_row)

        sheet = Tabular(matrix)
        sheet.write_xls(output_path)


    @staticmethod
    def _verified_file(file_path):
        if not file_path:
            return None
        file_path = abs_path(file_path)
        if not os.path.isfile(file_path):
            Colour.print('No such file : ' + Colour.END + file_path,Colour.RED)
            sys.exit()
        return file_path

