'''
This class reads in t1/t2 data
The main class imports the data read in here
'''


import csv


directory = '3p71_ga/'
partition = 't1'  # Edit this for problem data selection
path = directory + partition

courses = []
rooms = []
timeslots = []


class Course:
    def __init__(self, name, professor, students, duration):
        self.name = name
        self.professor = professor
        self.students = students
        self.duration = duration

class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

class TimeSlot:
    def __init__(self, day, hour):
        self.day = day
        self.hour = hour




#row_count ensures that col titles are not incl.
row_count = 0
with open(path + '/courses.txt', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row_count != 0:
            #each row in courses.txt is: name, professor, students, duration
            courses.append(Course(row[0], row[1], int(row[2]), int(row[3])))
        row_count = 1

row_count = 0
with open(path + '/rooms.txt', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row_count != 0:
            rooms.append(Room(row[0], int(row[1])))
        row_count = 1

row_count = 0
with open(path + '/timeslots.txt', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row_count != 0:
            timeslots.append(TimeSlot(row[0], int(row[1])))
        row_count = 1
 
 
'''        
print(courses)
print('---')
print(rooms)
print('---')
print(timeslots)
'''     
#These lists are imported in the main class        