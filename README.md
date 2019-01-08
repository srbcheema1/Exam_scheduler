# Exam_scheduler

[![a srbcheema1 production](https://img.shields.io/badge/-a%20srbcheema1%20production-blue.svg)](https://github.com/srbcheema1)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.ocm/srbcheema1/exam_scheduler/issues)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/srbcheema1/exam_scheduler)
[![Build Status](https://travis-ci.org/srbcheema1/exam_scheduler.svg?branch=master)](https://travis-ci.org/srbcheema1/exam_scheduler)
[![HitCount](http://hits.dwyl.io/srbcheema1/exam_scheduler.svg)](http://hits.dwyl.io/srbcheema1/exam_scheduler)

**exam_scheduler** is a commandline tool to produce teacher-duty schedule in examination for a school/college.


### Installation

#### Install using pip (Recommended)

- Use pip to install, user `--user` flag
```
python3 -m pip install --user exam_scheduler
```

#### Build from Source

- Clone the repository and checkout to stable commit
```
git clone https://github.com/srbcheema1/exam_scheduler
cd exam_scheduler
git checkout <latest_version say: v0.0.x>
```

- install requirements
```
python3 -m pip install --user -r requirements.txt
```
- Install exam_scheduler
```
python3 setup.py install --user
```
- Building Source Distribution
```
python3 setup.py sdist
```



### Inputs Required


- room_list - includes `room-name` and `teachers-required` as compulsory attributes. Other attributes may follow.

- teacher_list - includes `teacher-name` and `rank` as compulsory attributes. Other attributes may follow.

- schedule_list - A 2D matrix includeing relation between a session and a room, value is 'Y' if room is required on particular session.

#### Input can be provided in a xlsx or csv file

### Config files

- config.json - includes paths for input files in json format. default path ~/.config/exam_scheduler/config.json
```
{
    "room_list": "/home/srb/programs/exam_schedular/input/room_list.csv",
    "teacher_list": "/home/srb/programs/exam_schedular/input/teacher_list.csv",
    "schedule_list": "/home/srb/programs/exam_schedular/input/schedule_list.csv"
}
```
By default it will automtically pick files from working-directory OR input-folder containing `room_list`,`teacher_list`,`schedule_list` in their names.

- work_ratio.json - includes working ratio for different ranks with respect to rank `1`.
```
{
    "1": 100,
    "2": 150,
    "3": 200,
    "4": 250,
    "5": 300
}
```
This means if rank 1 will work for 100 units then rank 3 will work 200 units, simply rank 2 will work twice than rank 1.


### Usage
```
srb@srb-pc:$ exam_scheduler --help
usage: exam_scheduler.py [-h] [-v] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display version number
  -o OUTPUT, --output OUTPUT
                        Output file name, default output.xlsx
```
```
srb@srb-pc:$ exam_scheduler -o result.xlsx
Using room_list : /home/srb/programs/exam_schedular/input/room_list.csv
Using teacher_list : /home/srb/programs/exam_schedular/input/teacher_list.csv
Using schedule_list : /home/srb/programs/exam_schedular/input/schedule_list.csv
Output written to : /home/srb/programs/exam_schedular/result.xlsx
```



### Contact / Social Media

[![Github](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/github.png)](https://github.com/srbcheema1/)
[![LinkedIn](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/linkedin-48x48.png)](https://www.linkedin.com/in/srbcheema1/)
[![Facebook](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/fb.png)](https://www.facebook.com/srbcheema/)


### Developed by

Developer / Author: [Srb Cheema](https://github.com/srbcheema1/)
