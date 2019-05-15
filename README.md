# Exam_scheduler

[![a srbcheema1 production](https://img.shields.io/badge/-a%20srbcheema1%20production-blue.svg)](https://github.com/srbcheema1)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.ocm/srbcheema1/exam_scheduler/issues)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/srbcheema1/exam_scheduler)
[![Build Status](https://travis-ci.org/srbcheema1/exam_scheduler.svg?branch=master)](https://travis-ci.org/srbcheema1/exam_scheduler)
[![HitCount](http://hits.dwyl.io/srbcheema1/exam_scheduler.svg)](http://hits.dwyl.io/srbcheema1/exam_scheduler)

**exam_scheduler** is a commandline tool to produce teacher-duty schedule in examination for a school/college. It also acts as library-cum-backbone for [ExamScheduler](https://srbcheema1.github.io/ExamScheduler/) a web-based tool.


### Installation

#### Install using pip (Recommended)

- Use pip to install, user `--user` flag
```
python3 -m pip install --user exam_scheduler
```


##### linux and mac users
```
python3 -m pip install --user exam_scheduler
```
Don't forget `~/.local/bin` should be in your `PATH`. Add line `export PATH=$PATH:"~/.local/bin"` in your `.bashrc`

##### windows users
for windows users you should have python3 installed in your system
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

- teachers_list - includes `teacher-name` and `rank` as compulsory attributes. Other attributes may follow.

- schedule_list - A 2D matrix includeing relation between a session and a room, value is 'Y' if room is required on particular session.

- work_ratio - Includes rank and work_ratio as compulsory attributes. Other optional attributes may follow.

By default it will automtically pick excel files from working-directory OR `input` folder containing `room_list`,`teachers_list`,`schedule_list` and `work_ratio` in their names.

For more instructions please visit our [help page](https://srbcheema1.github.io/ExamScheduler/#/Help).

### Usage
```
srb@srb-pc:$ exam_scheduler --help
usage: exam_scheduler.py [-h] [-v] [-o OUTPUT] [-s SEED] [-r RESERVED]
                         [-vr VR | -vs VS | -vt VT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display version number
  -o OUTPUT, --output OUTPUT
                        Output file name, default output.xlsx
  -s SEED, --seed SEED  seed value for randomness
  -r RESERVED, --reserved RESERVED
                        reserved number of seats for each session
  -d, --debug           print debug info
  -vr VR                verify room_list file
  -vs VS                verify schedule_list file
  -vt VT                verify teachers_list file
```

```
srb@srb-pc:$ exam_scheduler -o result.xlsx
Using room_list : /home/srb/programs/exam_scheduler/input/room_list.csv
Using teachers_list : /home/srb/programs/exam_scheduler/input/teachers_list.csv
Using schedule_list : /home/srb/programs/exam_scheduler/input/schedule_list.csv
Using seed value : 5
Using reserved value : 0
rank count : {
   "0": 33,
   "1": 7,
   "2": 23,
   "3": 77,
   "4": 59,
   "5": 91
}
average duties : {
   "0": 0.0,
   "1": 2.0,
   "2": 2.347,
   "3": 3.0,
   "4": 3.0,
   "5": 3.0
}
type of rooms : {
   "[1, 3, 5]": 1,
   "[1, 4, 5]": 13,
   "[2, 3, 5]": 1,
   "[2, 4, 5]": 53,
   "[3, 4, 5]": 85,
   "[3, 4]": 25,
   "[3, 5]": 119,
   "[4, 5]": 1
}
Output written to : /home/srb/programs/exam_scheduler/result.xlsx
```



### Contact / Social Media

[![Github](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/github.png)](https://github.com/srbcheema1/)
[![LinkedIn](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/linkedin-48x48.png)](https://www.linkedin.com/in/srbcheema1/)
[![Facebook](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/fb.png)](https://www.facebook.com/srbcheema/)


### Developed by

Developer / Author: [Srb Cheema](https://github.com/srbcheema1/)

Collaborator : [Rakesh Kumar](https://github.com/spider34/)
