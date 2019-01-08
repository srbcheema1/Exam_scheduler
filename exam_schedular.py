#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from exam_schedular import *
from exam_schedular.session import Session


if __name__ == "__main__":
    # from exam_schedular.main import main
    # main()
    session_list = Session.get_sessions('input/rooms_need.csv','input/nith_rooms.csv')
    print(session_list[0])
    print(session_list[2])
    print(session_list[2].room_list[0])
