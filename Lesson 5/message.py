from collections import namedtuple

# Raw input
names = input('Enter names seperated by commas: ')
assignments = input('Enter assignment counts seperated by commas: ')
grades = input('Enter grades seperated by commas: ')

# Process Raw input
names = [name.strip().title() for name in names.split(',')]
assignments = list(map(int, assignments.split(',')))
grades = list(map(int, grades.split(',')))

# create a named tupled list for the students
Student = namedtuple('Student', 'name assignment grade')
students = [Student(*i) for i in zip(names, assignments, grades)]

# message string to be used for each student
# HINT: use .format() with this string in your for loop
message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"

# write a for loop that iterates through
# each set of names, assignments, and grades to print each student's message
for student in students:
    potential_grade = student.grade + (2*student.assignment)
    print(message.format(
        student.name,
        student.assignment,
        student.grade,
        potential_grade))
