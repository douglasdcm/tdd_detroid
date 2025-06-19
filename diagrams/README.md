It is necessary to install `draw.io` extension to edit the files

# Core entities
Represent the main `nouns` present in the requirements
- Administrator
- Coordinator
- Coordinator's Report
- Course
- Course Coordinator
- Course Unique Identifier
- External CPF validation Sytem (Government System)
- Enrollment List
- General Coordinator
- Grade Control (GPA)
- Semester
- Student
- Student Grade
- Student Credential
- Student Hstory
- Subject
- Subject Unique Identifier
- Student's Situation
- Student Documentation
- System
- Units
- University
- Teacher
- Teacher Credential
- Coordinator Credential

# States
Represents the state for each core entity
- Coordinator: do not coordinate Courses, coordinate less than the maximum value of Courses, coordinate maximum value of Courses, coordinates more tham the maximum value of Courses
- Course: locked, unlocked, cancelled, not cancelled, has Coordinator, does not have Coordinator, has minimun value of Subject, does not have minumum value of Subjects, has minimum Students, does not have minimum Students
- Grade: under minimum value, between minimum and maximum values, above maximum value, can update, can not upate
- General Coordinator: is coordinator of Course (forbiden), is not Coordinator of Course
- Student: approved, reproved (failed), enrolled, not enrolled, has missing Subjects, does not have missing Subjects, has maximum value of Semester, does not have maximum value of Semeter
- Subject: can update, can not update, has minimum enrolled Students, does not have minimum enrolled Students, has enrolled Students over the maximum value, locked, unlocked
- University: does not have Courses, does not have Subcjets, has maximum value of Courses, has maximum value of Subjects, does not have maximum value of Courses, does not have maximum value of Subjects 

# Actions
Represent the actions each entity can do or suffer
- Adminstrator: list all Students, list all Courses, list Student per Course, list Subjects per Student, list all Course Coordinator, 
- Course Coordinator: list students, list grades of Subjects, list GPA of Students, remove Subjects, accept Student, do not accept Student, add Subject to their Course
- Student: lock the Course, update Grades, enroll in Course, enroll in maximum value of Subject, does not enroll in maximum value of Subject, create Student, list all their Subjects by Course, list all taken Subjects, (do not) take Subject?, list missing Subjects, authenticate
- General Coordinator: list all Courses, list Students, list Grades of Subjects, list GPA of Students, cancel Course, create Course, open Semester, close Semester, add Student to Enrollment List, analise Student Documentation?, add Course to University
- Coordinator: coordinate, list students of their Courses, list subjects of their Courses, list grades of their Courses, list GPA of their Courses, authenticate
- Teacher: set the Grade of Students in their Subject, teach maximum vallue of subject, does not teach maximum value of subject
- Teacher: authenticate