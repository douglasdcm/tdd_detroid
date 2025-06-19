It is necessary to install `draw.io` extension to edit the files

# Taxonomy
- Core entities: represent the main `nouns` present in the requirements
- States: represents the state for each core entity
- Actions: represent the actions each entity can do or suffer

# Core Entities
## Administrator
### Actions
- list all Students
- list all Courses
- list Student per Course
- list Subjects per Student
- list all Course Coordinator 


## Coordinator
### State
- do not coordinate Courses
- coordinate less than the maximum Courses
- coordinate maximum Courses,
- coordinates more tham the maximum value of Courses
### Actions
- coordinate
- list students of their Courses
- list subjects of their Courses
- list grades of their Courses
- list GPA of their Courses
- authenticate

## Coordinator's Report
## Course
### State
- locked
- unlocked
- cancelled
- not cancelled
- has Coordinator
- does not have Coordinator
- has minimun Subject
- does not have minumum Subjects
- has minimum Students
- does not have minimum Students

## Course Coordinator
### Actions
- list students
- list grades of Subjects
- list GPA of Students
- remove Subjects
- accept Student
- do not accept Student-
- add Subject to their Course

## Course Unique Identifier
## External CPF validation Sytem (Government System)
## Enrollment List
## General Coordinator
### State
- is coordinator of Course (forbiden)
- is not Coordinator of Course

### Actions
- list all Courses
- list Students
- list Grades of Subjects
- list GPA of Students
- cancel Course
- create Course
- open Semester
- close Semester
- add Student to Enrollment List
- analise Student Documentation?
- add Course to University

## Grade Control (GPA) (Grade?)
### State
- under minimum value
- between minimum and maximum values
- above maximum value
- can update
- can not upate

## Semester
## Student
### State
- is not enrolled in maximum Subject
- enrolled in maximum Subject
- approved
- reproved (failed)
- enrolled
- not enrolled
- has missing Subjects
- does not have missing Subjects
- has maximum Semester
- does not have maximum Semeter
### Actions
- lock the Course
- update Grades
- enroll in Course
- create Student
- list all their Subjects by Course
- list all taken Subjects
- (do not) take Subject?
- list missing Subjects
- authenticate

## Student Grade
## Student Credential
## Student History

## Subject
### State
- can update
- can not update
- has minimum enrolled Students
- does not have minimum enrolled Students
- has enrolled Students over the maximum value
- locked
- unlocked

## Subject Unique Identifier
## Student's Situation
## Student Documentation
## System
## Units

## University
### State
- does not have Courses
- does not have Subcjets
- has maximum Courses
- has maximum Subjects
- does not have maximum Courses
- does not have maximum Subjects 

## Teacher
### Actions
- set the Grade of Students in their Subject
- teach maximum Subject
- does not teach maximum Subject
- authenticate

## Teacher Credential
## Coordinator Credential










