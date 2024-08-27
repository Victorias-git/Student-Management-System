import uuid

class Person:
    """
    A base class representing a person with attributes name and ID_number.
    """
    def __init__ (self, name, ID_number):
        self.name = name
        self.ID_number = ID_number  


class Student(Person):
    """
    A class to represent a student, which inherits attributes from the class person and adds the major attribute. It maintains a count of created students.
    """
    count = 0
    def __init__ (self, name, ID_number, major):
        super().__init__ (name, ID_number)
        self.major = major
        Student.count += 1 ##Count number of students.

    @classmethod
    def get_count(cls):
        return f"Number of students: {cls.count}"

class Instructor(Person):
    """
    A class to represent a instructor, which inherits attributes from the class person and adds the department attribute. It maintains a count of created students.
    """
    count = 0
    def __init__ (self, name, ID_number, department):
        super().__init__ (name, ID_number)
        self.department = department
        Instructor.count += 1 ##Count number of instructors.

    @classmethod
    def get_count(cls):
        return f"Number of instructors: {cls.count}"

class Course:
    """
    Represents a course with attributes course_name, course_ID, and enrolled_students.
    Manages enrollment by adding or removing students from the course.
    Maintains a count to keep track of the number of courses created.
    """
    count = 0
    def __init__ (self, course_name, course_ID):  ##This is the constructor of the Course class. It initializes three instance attributes.
        self.course_name = course_name
        self.course_ID = course_ID
        self.enrolled_students = [] ## Initialize enrolled_students as an empty list
        Course.count += 1 ##Count number of offered courses.

    @classmethod
    def get_count(cls):
        return f"Number of offered courses: {cls.count}"
        
    def add_student (self, student:Student) -> None: ##adding students to course
        self.enrolled_students.append(student)
    def remove_student (self, student:Student)-> None: ##removing students to course
        self.enrolled_students.remove(student)

    def __str__(self): ##the __str__ method to return a string representation of the course.
        student_names = ', '.join([student.name for student in self.enrolled_students]) ## join names into a single string, separated by commas. 
        return f"Course Name: {self.course_name} - Course ID: {self.course_ID}, Enrolled Students: {student_names}"

class Enrollment:
    """
    Represents the enrollment of a student in a course, storing the student, course ID, and grade.
    This class is used to link students to courses and manage their grades.
    """
    def __init__ (self, student, course_ID: str, grade: float = None) -> None: ##This is the constructor of the Enrollment class. It initializes three instance attributes.
        self.ID_number = student
        self.course_ID = course_ID
        self.grade = grade
        

    def __str__(self): ## to return a string representation of the enrollment.
         return f"Student: {self.ID_number.name}, Course: {self.course_ID}, Grade: {self.grade}"

class StudentManagementSystem:
    """
    A class to manage students, instructors, courses, and enrollments.
    """
    def __init__(self):
        self.students = {} ##Key: ID_number, Value: Student
        self.instructors = {} ##Key: ID_number, Value: Instructor
        self.courses = {} ##Key: course_ID, Value: Course
        self.enrollments = {}  ##Key: (student_id, course_id), Value: grade

    def add_student(self, student: Student) -> None:
        if student.ID_number in self.students:
            raise ValueError("student already exist.")
        self.students[student.ID_number] = student

    def remove_student(self, ID_number:str) -> Student | None:
    ##Searches for ID and removes a student from the system if ID found.

        if ID_number in self.students:
            del self.students[ID_number]
            

    def update_student(self, ID_number, new_name = None, new_major = None) -> None:
    ####
        if ID_number in self.students:
            if new_name:
                self.students[ID_number].name = new_name
            if new_major:
                self.students[ID_number].major = new_major
        else:
            return None


    ###INSTRUCTOR UPDATE
    def add_instructor(self, instructor: Instructor) -> None:
        if instructor.ID_number in self.instructors:
            raise ValueError("instructor already exist.")
        self.instructors[instructor.ID_number] = instructor

    def remove_instructor(self, ID_number:str) -> Instructor | None:
    ##Searches for ID and removes an instructor from the system if ID found.

        if ID_number in self.instructors:
            del self.instructors[ID_number]


    def update_instructor(self, ID_number, new_name = None, new_department = None,) -> None:
    ####
        if ID_number in self.instructors:
            if new_name:
                self.instructors[ID_number].name = new_name
            if new_department:
                self.instructors[ID_number].department = new_department
        else:
            return None

###COURSE UPDATE
    def add_course(self, course= Course) -> None:
        if course.ID_number in self.courses:
            raise ValueError("course already exist.")
        self.courses[course.course_ID] = course

    def remove_course(self, course_ID:str) -> Course | None:
    ##Searches for ID and removes course from the system if ID found.

        if course_ID in self.courses:
            del self.courses[course_ID]
        

    def update_course(self, course_ID:str, new_course_name = None, new_students_ID = None, ID_number = None) -> None:
    ####
        if course_ID in self.courses:
            if new_course_name:
                self.courses[course_ID].course_name = new_course_name
            if new_students_ID:
                self.courses[course_ID].add_student(new_students_ID)
            if ID_number:
                self.courses[course_ID].remove_student(ID_number)
        
    ##Enroll students in courses
    def enroll_student(self, student: Student, course_ID:str, grade: float = None) -> None: ##This method enrolls a student in a course.
        enrollment = Enrollment(student, course_ID, grade)  # Created an enrollment object.
        self.enrollments[(student.ID_number, course_ID)] = enrollment ##storing enrollment information in a dictionary.
        
        
    ##Assign grades to students for specific courses 
    def assign_grade(self, ID_number:str, course_ID:str, grade: float) -> None: ##This method assigns a grade to a student for a specific course.
        if (ID_number, course_ID) in self.enrollments: ##checks if the student-course combination exists in the enrollments dictionary.
            self.enrollments[(ID_number, course_ID)].grade = grade ##If it exists, we update the grade attribute.

    ##Retrieve a list of students enrolled in a specific course
    def get_students_in_course(self, course_ID:str) -> list: ##This method retrieves a list of students enrolled in a specific course.
        students = []
        for enrollment in self.enrollments.values():
            if enrollment.course_ID == course_ID:
                students.append(self.students[enrollment.ID_number])
        return students ##It iterates through enrollments dictionary, if the course_ID is found it returns the list of students enrolled in the course.

    ##Retrieve a list of courses a specific student is enrolled in
    def get_courses_for_student(self, ID_number:str) -> list:
        courses = []
        for enrollment in self.enrollments.values():
            if enrollment.ID_number == ID_number:
                courses.append(self.courses[enrollment.course_ID])
        return courses ##It iterates through enrollments dictionary, if the course_ID is found it returns the list of courses the student is enrolled in.


sms = StudentManagementSystem()

#Creating students
student1 = Student("Victoria", "DE/2024/001", "Data Engineering")
student2 = Student("John", "AT/2024/002", "Arts")

#Creating instructors 
instructor1 = Instructor("Grace", "INST/001", "Science")
instructor2 = Instructor("Adam", "INST/002", "Arts")

#Creating courses
course1 = Course("Introduction to Data", "DATA101")
course2 = Course("Sketching", "SKT111")
course3 = Course("SQL", "SQL111")
course4 = Course("Painting", "PT111")

# Enroll students in courses
sms.enroll_student(student1, course1.course_ID, 52)
sms.enroll_student(student1, course3.course_ID, 78)
sms.enroll_student(student2, course2.course_ID, 81)
sms.enroll_student(student2, course4.course_ID, 73)


print(Student.get_count())
print(Instructor.get_count())
print(Course.get_count())


