import os
import sys
import json

from srblib import abs_path
from srblib import Colour
from srblib import SrbJson
from srblib import Tabular
from srblib import debug

from .constants import max_adv, seed_val_var
from .priority_queue import PriorityQueue, Queue, EmptyQueue
from .session import Session
from .teacher import Teacher
from .util import randomize, fabricate, fabricate_adv
from .verifier import Compiler
from .work_ratio import WorkRatio

class Scheduler:
    def __init__(self,seed=5,reserved=0,room_list=None,teachers_list=None,schedule_list=None,work_ratio=None):
        self.debug = False
        self.seed = int(seed)
        self.reserved = int(reserved)
        self.room_list = Scheduler._verified_file(room_list)
        self.teachers_list = Scheduler._verified_file(teachers_list)
        self.schedule_list = Scheduler._verified_file(schedule_list)
        self.work_ratio = Scheduler._verified_file(work_ratio)
        self.workratio = None
        self.adv = max_adv # used in round_n_robin for advanced algo.

    def _configure_paths(self):
        '''
        to be called manually, not to be used in library
        '''
        from .configurations import config_json
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
        var_list = ['room_list','teachers_list','schedule_list','work_ratio']
        for var_name in var_list:
            configure_path(var_name)
            Colour.print('Using ' + var_name + ' : ' + Colour.END + getattr(self,var_name), Colour.GREEN)
        Colour.print('Using seed value : ' + Colour.END + str(self.seed), Colour.GREEN)
        Colour.print('Using reserved value : ' + Colour.END + str(self.reserved), Colour.GREEN)


    def compileall(self):
        res = Compiler.compile_room_list(self.room_list)
        if not res: return res
        res = Compiler.compile_work_ratio(self.work_ratio)
        if not res: return res
        res = Compiler.compile_teachers_list(self.teachers_list)
        if not res: return res
        res = Compiler.compile_schedule_list(self.schedule_list)
        if not res: return res
        res = Compiler.crosscompile(self.teachers_list,
                                    self.room_list,
                                    self.schedule_list,
                                    self.work_ratio
                                    )
        return res



    def try_schedule(self, output_path):
        try:
            self._schedule(output_path)
            Colour.print('Final adv value is '+str(self.adv),Colour.YELLOW)
            Colour.print('Final seed value is '+str(self.seed),Colour.YELLOW)
            return True
        except EmptyQueue:
            return False

    def schedule(self,output_path):
        self.adv = max_adv
        seed = self.seed
        while self.adv >= 0:
            Colour.print('Trying adv as '+str(self.adv),Colour.YELLOW)
            for i in range(seed,seed + seed_val_var):
                self.seed = i
                if self.try_schedule(output_path):
                    return
            self.seed = seed-1
            if self.try_schedule(output_path):
                return
            self.adv -= 1
        self.seed = seed
        self._schedule(output_path)

    def _schedule(self,output_path):
        self.workratio = WorkRatio(self.work_ratio)
        teachers_list = Teacher.get_teachers(self.teachers_list,self.workratio)
        session_list = Session.get_sessions(self.schedule_list,self.room_list,self.workratio)

        # for scheduling reserved using -r option
        self.schedule_reserved_random(teachers_list,session_list)

        # fake run
        self.generate_duties(teachers_list,session_list)

        # round_n_robin algorithm
        self.round_n_robin(teachers_list,session_list)

        # finished processing ... finally create output
        self.dump_output(teachers_list,session_list,output_path)


    def round_n_robin(self,teachers_list,session_list):
        '''
        Srb's round-n-robin algorithm
        self.adv means advance, it will not allow teachers in same session for that number of times
        '''
        sorted_teachers_list = fabricate(teachers_list[:],self.seed)
        sorted_teachers_list.sort(key=lambda x: int(x.rank))
        session_pq = PriorityQueue(fabricate_adv(session_list,lambda x: x.batch,self.seed))

        def debug_pq(pq):
            if not self.debug: return
            need = 0
            for item in pq._data:
               session = item[1]
               for room in session.room_list:
                   need += room.unfilled()
            print('Session PQ has rooms: ',need)

        debug_how = 0
        for session in session_list:
            for room in session.room_list:
                debug_how += room.teachers

        for teacher in sorted_teachers_list:
            done_list = []
            for _ in range(teacher.duties):
                session = session_pq.pop()
                adv = self.adv
                while(session.name in teacher.alloted_res or (adv > 0 and  session.base in teacher.alloted_base)):
                    adv -= 1
                    if(self.debug):
                        if session.base in teacher.alloted_base:
                            print('same day ',end='')
                        print('skipped session')
                        print(session)
                    done_list.append(session)
                    session = session_pq.pop()

                if(self.debug): print(session)
                done_list.append(session)

                room = session.room_pq.pop()
                room.teachers_alloted.append(teacher)
                teacher.alloted[session.name] = room.name
                teacher.alloted_base.add(session.base)
                session.remaining -= 1
                debug_how -= 1
                if room.unfilled() > 0: session.room_pq.push(room)
            for session in done_list:
                if session.remaining > 0: session_pq.push(session)
            if(self.debug):print(teacher)
            if(self.debug):print('debug_how',debug_how)
            if(self.debug):debug_pq(session_pq)
            if(self.debug):print('\n')


    def dump_output(self,teachers_list,session_list,output_path):
        matrix = [["Name of Faculty Member","Info"]]
        if debug: matrix[0].extend(['_rank','_total','_res','_credits']) # srbdebug

        dmap = {} # map to contain count of avg duties of some rank
        rmap = {} # map to contain count of teachers of some rank
        for teacher in teachers_list:
            rmap[teacher.rank] = 0
            dmap[teacher.rank] = 0
        for teacher in teachers_list:
            rmap[teacher.rank] += 1
            dmap[teacher.rank] += teacher.duties
        def divide(a,b):
            a = int((a*1000)/b)
            return a/1000
        for rank in rmap:
            dmap[rank] = divide(dmap[rank],rmap[rank])

        tmap = {} # map to contain count of room types
        for session in session_list:
            matrix[0].append(session.name)
            for room in session.room_list:
                if room.reserved:
                    continue
                if room.get_type() in tmap:
                    tmap[room.get_type()] += 1
                else:
                    tmap[room.get_type()] = 1

        matrix[0].append("Total")
        matrix[0].append("mail")
        same_day_duties = self._get_same_day_multiple_duties(teachers_list)
        if(same_day_duties): matrix[0].append("s_d_m_d")


        for teacher in teachers_list:
            teachers_row = [teacher.name,teacher.info]
            if teacher.duties != len(teacher.alloted) - len(teacher.alloted_res):
                print('ERROR: teacher unable to get enough slots as anticipated')
                print(teacher)
                raise Exception('ERROR: teacher unable to get enough slots as anticipated')
            if debug:
                teachers_row.extend([
                    teacher.rank,
                    len(teacher.alloted),
                    len(teacher.alloted_res),
                    int(teacher._credits),
                ])
            for session in session_list:
                if session.name in teacher.alloted: teachers_row.append(teacher.alloted[session.name])
                else: teachers_row.append('-')
            teachers_row.append(len(teacher.alloted))
            teachers_row.append(teacher.mail)
            if(same_day_duties):
                same_day_duties_t = 0 # compute same day duties per teacher
                sess_set = set()
                for session_name in teacher.alloted.keys():
                    if Session.get_base(session_name) in sess_set:
                        same_day_duties_t += 1
                        continue
                    sess_set.add(Session.get_base(session_name))
                teachers_row.append(same_day_duties_t)
            matrix.append(teachers_row)

        lmap = json.dumps(rmap,indent=3,sort_keys=True)
        Colour.print('rank count : ',Colour.CYAN,end='')
        Colour.print(lmap,Colour.GREEN)

        lmap = json.dumps(dmap,indent=3,sort_keys=True)
        Colour.print('average duties : ',Colour.CYAN,end='')
        Colour.print(lmap,Colour.GREEN)

        lmap = json.dumps(tmap,indent=3,sort_keys=True)
        Colour.print('type of rooms : ',Colour.CYAN,end='')
        Colour.print(lmap,Colour.GREEN)

        matrix.extend([[],[],['','rank','count','avg duties']])
        for key in sorted(rmap):
            matrix.append(['',key,rmap[key],dmap[key]])

        matrix.extend([[],[],['','type of room','number']])
        for key in sorted(tmap):
            matrix.append(['',key,tmap[key]])

        if same_day_duties > 0:
            Colour.print('Got '+str(same_day_duties)+' same-day-duties',Colour.YELLOW)
            matrix.extend([[],[],['','WARNING:','Adv-algo value was '+str(self.adv)]])
            matrix.extend([['','','You may get teacher duty multiple in a day']])
            matrix.extend([['','','We got '+str(same_day_duties) + ' such cases']])
            matrix.extend([['','','Please visit s_d_m_d(same-day-multiple-duties) column for number of such cases per teacher']])

        matrix.extend([[],[],['','Help:','In case help required please visit help section on website']])
        matrix.extend([['','','In case of unsatisfactory results please contact srbcheema2@gmail.com']])
        matrix.extend([[],[],['','','a srbcheema1 Production']])

        sheet = Tabular(matrix)
        sheet.write_xls(output_path)


    def generate_duties(self,teachers_list,session_list):
        '''
        Fake run: just to determine teacher duties number
        '''
        teachers_pq = PriorityQueue(randomize(teachers_list,self.seed))
        for session in session_list:
            done_list = []
            for room in session.room_list:
                if room.reserved: continue # continue for reserved rooms
                for _ in range(room.teachers):
                    teacher = teachers_pq.pop()
                    while session.name in teacher.alloted_res: # teacher should not get sametime res and room
                        done_list.append(teacher)
                        teacher = teachers_pq.pop()
                    teacher._credits += self.workratio.credits_calc(teacher.rank)
                    teacher.duties += 1
                    done_list.append(teacher)
            for teacher in done_list:
                teachers_pq.push(teacher)


    def schedule_reserved_random(self,teachers_list,session_list):
        '''
        this res is triggered using -r, it will be alloted randomly
        there is another way, that is using creating a RES room in roomlist (not recommended)
        both differ by name Res for this one RES for that one

            reason for not being recommended theh roomlist way of reserving:
                1. unequal distribution of reserved seats
                2. less credits for reserved
                3. makes priority queue difficult to schedule if reserved room contain more teachers than other rooms
        '''
        teachers_reserved_q = Queue(randomize(teachers_list,self.seed+1))
        for session in session_list: # reserve
            for _ in range(self.reserved): # fixed reserves per day (only for commanline users)
                teacher = teachers_reserved_q.pop()
                while teacher.rank == 0:
                    teacher = teachers_reserved_q.pop()
                teachers_reserved_q.push(teacher)
                teacher.alloted[session.name] = '_Res'
                teacher.alloted_res.add(session.name)
                teacher.alloted_base.add(session.base)
                teacher._credits += self.workratio.credits_calc(teacher.rank) / 2
            for room in session.room_list:
                if room.reserved:
                    for _ in range(room.teachers):
                        teacher = teachers_reserved_q.pop()
                        while teacher.rank == 0:
                            teacher = teachers_reserved_q.pop()
                        teachers_reserved_q.push(teacher)
                        teacher.alloted[session.name] = room.name
                        teacher.alloted_res.add(session.name)
                        teacher.alloted_base.add(session.base)
                        teacher._credits += self.workratio.credits_calc(teacher.rank) / 2
                        room.teachers_alloted.append(teacher)
                        session.remaining -= 1
            session.room_pq.sync()


    @staticmethod
    def _verified_file(file_path):
        if not file_path:
            return None
        file_path = abs_path(file_path)
        if not os.path.isfile(file_path):
            Colour.print('No such file : ' + Colour.END + file_path,Colour.RED)
            sys.exit()
        return file_path

    @staticmethod
    def _get_max_rank(teachers_list):
        max_rank = 0
        for teacher in teachers_list:
            max_rank = max(max_rank,teacher.rank)
        return max_rank

    def _get_same_day_multiple_duties(self,teachers_list):
        same_day_duties = 0
        for teacher in teachers_list:
            same_day_duties_t = 0 # compute same day duties per teacher
            teacher_satisfied = True
            sess_set = set()
            for session_name in teacher.alloted.keys():
                if Session.get_base(session_name) in sess_set:
                    same_day_duties_t += 1
                    teacher_satisfied = False
                    continue
                sess_set.add(Session.get_base(session_name))
            if not teacher_satisfied:
                if(self.debug): print(teacher)
            same_day_duties += same_day_duties_t
        return same_day_duties

