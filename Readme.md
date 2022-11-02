# CSP Time Tabling Problem

## Problem Description
Suppose you need to develop a timetable for a semester.
There is a list of subjects, a set of possible time slots for each subject and a set of rooms. 
<br/>Some subjects are compulsory while some are optional. <br/>
<br/>
Following are the constraints to satisfy.
<br/>
1. A given subjects can be assigned only to one of the possible time slots given for that subject. 
2. Two compulsory subjects cannot be in the same time slot (optional subjects may). 
3. Two subjects cannot be assigned to the same room if they are assigned to the same time slot

## Executing the program
```bash
.\assign_halls.exe -h
```

```
usage: assign_halls.py [-h] input.csv [output.csv]

CSP Time Tabling Problem

positional arguments:
  input.csv   csv file containing raw data.
                       * Format of records: <subject_x>,<compulsory[C]/ optional[O]> [one or more time slots]
                       * Last line available rooms as R1, R2, etc.
  output.csv  csv file to write the generated time table.
                       Format of entries: <subject_x>, <time_slot>, <room_assigned>

optional arguments:
  -h, --help           show this help message and exit

```