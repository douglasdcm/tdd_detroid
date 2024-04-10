{Translated from Portuguese to English using AI}
# College Student Grade Control
## Introduction
This project aims to practice "code smells" related to unit tests using an application that simulates a real business scenario.
The code will be developed using the TDD technique in the Detroit style, hence the name of the repository.
The application simulates the control of grades for university students.

# Installation
```
# create database
sqlite3 university.db
sqlite> .quit
```

# CLI Usage
```
python cli.py --help
Usage: cli.py [OPTIONS]

Options:
  --name TEXT               Name of the student.
  --cpf TEXT                CPD of the student.
  --course-identifier TEXT  Course number identifier.
  --help                    Show this message and exit.


# enroll student to course
python cli.py --name any --cpf 123.456.789-10 --course-identifier any

```


Below is the specification of the application:
Definition of Done:
1. Unit tests cover the functionality.
2. The functionality is developed to be used via CLI (Command Line Interface).
3. Data is being saved in the database.
# Deliverables
Construction of the basic functions of the system
1. Each student will have a grade control called "grade point average" (GPA).
2. The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.
3. The student is considered approved at the university if their GPA is above or equal to 7 (seven) at the end of the course.
4. If a student takes the same subject more than once, the highest grade will be considered in the GPA calculation.
<!-- Required setup to allow enrollments -->
5. Initially, the university will have 3 courses with 3 subjects each.
6. Subjects in each course may have the same names but will be differentiated by a unique identifier (niu).
7. The system must calculate the student's situation taking into account the subjects taken and the total number of subjects in each course.
8. The student can only take subjects from their course.
9. Courses must have a unique identifier and name.
10. ~~Course~~ Subject names can be the same, but the unique identifier for each ~~course~~ subject must be different.
11. A course cannot have two subjects with the same name, even if the niu is different.
12. The maximum grade for a student in a subject is 10.
13. The minimum grade for a student in a subject is 0.
14. The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
15. The course coordinator can list the students, grades in each subject, and GPAs of the students.
16. The student can unlock the course, and their situation returns to the previous state.
17. Students must have names.
18. The general coordinator can list all courses, students, grades in each subject, and GPAs of each student.
19. The course coordinator can remove subjects, and in this case, students cannot update their grades in that subject.
20. Students can only update their grades in the subjects they are enrolled in.
21. Course and subject names must have a maximum of 10 letters.
22. Courses can have the same names if they are from different units.
<!-- The student can do any time. Don't need to wai the next semester -->
23. The student can only enroll in one course.
24. The coordinator can coordinate a maximum of three courses.
25. The coordinator can list the students, subjects, grades, and GPAs of all their courses (coordinator of more than one course).
<!-- this requirement wasn't informing the actor. Figured out while making the diagrams of use cases -->
<!-- 26. The course can be canceled. -->
26. The course can be canceled by the general cordinator.
27. Canceled courses cannot accept student enrollments.
<!-- How o set coordinators? -->
28. Canceled courses cannot have coordinators.
29. Each subject can have a maximum of 30 enrolled students.
30. The student must enroll in a minimum of 3 subjects.
31. If the number of subjects missing for a student is less than 3, they can enroll in 1 subject.
32. If the student does not enroll in the minimum number of subjects per semester, they will be automatically failed.
33. The student must have a validated CPF (Brazilian Social Security Number) in the external CPF validation system (government system).
34. Add the course name to the coordinator's reports.
35. The student is only approved if they achieve the minimum grade in all course subjects, even if their GPA is above the minimum.
36. The ~~user~~ student (person) must be able to create students with basic information.
<!-- The basic information is enough for enrollment -->
37. ~~The user must be able to enroll the student in a course.~~
38. The ~~user~~ general coordinator must be able to create courses with the minimum number of subjects.
39. The administrator, and only the administrator, must be able to list all students with detailed information (all available information).
40. The administrator, and only the administrator, must be able to list all courses with all available information.
41. The administrator, and only the administrator, must be able to list the list of students per course.
42. The administrator, and only the administrator, must be able to list the list of subjects per student.
43. The student must be able to list all subjects only from their course.
44. The student must be able to list all subjects they have taken.
45. The student must be able to list the missing subjects.
46. The administrator must be able to list all course coordinators with available information.
47. The student has 10 semesters to graduate.
48. If the student exceeds the 10 semesters, they are automatically failed.
49. The coordinator can only coordinate a maximum of 3 courses.
50. The general coordinator cannot be a coordinator of courses.