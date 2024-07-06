# Control of grades of college students

## Introduction
The application simulates the control of students' grades at a university. Check at the end the specification of the application:

# How to use it

## Option 1: docker-compose
Run the commnands and access "http://localhost:5000"
```
chmod +x utils/build_container.sh
./utils/build_container.sh
pip install build
./utils/build_dist.sh
docker-compose up -d
```

## Option 2: locally by Live Server
1. At the root of the project, run the commands below:
```
python3.6 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
python -m build
cp -r dist/ src/ui/
```
2. This project was developed using VSCode, so install [Live Server](https://github.com/ritwickdey/vscode-live-server-plus-plus) on VSCode
3. Navigate to the index.html file and start the Live Server as per the documentation
4. Fill in the form and confirm to see the records created

## Option 3: locally by Flask
1. Run the commands above to setup the application
2. Start the aplication running the commnad bellow and access "http://localhost:5001"
```
python app.py
```

## Option 4: by CLI
5. It is possible to interact with the application using the command line. See more details in the help menu.
```
python cli. init-bd
python cli.py --help
```

# Technologies
This project uses pure Python in the backend, html for the screens, sqlite to store the records, PyScript to create the elements of the screens, Liver Server, docker-compose to bring the application up.

# Limitations
When used by the graphical interface, the inserted records are lost every time the screen is rendered. Persistence is only possible when used from the command line

# Specification
Construction of the basic functions of the system (The features scratched are the ones implemented)
1. ~~Each student will have a grade control called "performance coefficient" (CR)~~
2. ~~The CR is the average of the student's grades in the subjects already taken~~
3. The student is considered approved at the university if his CR is above or equal to 7 (seven) at the end of the course
4. ~~If the student takes the same subject more than once, the highest grade will be considered in the calculation of the CR~~
5. ~~The faculty will initially have 3 courses with 3 subjects each~~
6. ~~The subjects of each course may have the same names, but they will be differentiated by the unique identifier number (niu)~~
7. The system should calculate the student's situation taking into account the subjects taken and the total number of subjects in each course
8. The student will only be able to attend subjects of his/her course
9. ~~The courses must have a unique identifier and name~~
10. ~~The course names can be the same, but the unique identifier of each course must be different~~
11. ~~A course cannot have two subjects with the same name, even if the niu is different~~
12. ~~A student's maximum grade in a subject is 10~~
13. ~~A student's minimum grade in a subject is 0~~
14. The student can lock the course and in this case he cannot update his grades or subjects taken
15. The course coordinator can list the students, grades in each subject and students' credits.
16. The Student can unlock the course and their situation reverts to the previous one
17. ~~Students must have names~~
18. The general coordinator can list the students and grades in each subject and credit of each student from all courses
19. The course coordinator can eliminate subjects and in this case students cannot update their grades in this subject
20. Students can only update their grades in the subjects they are enrolled in
21. The name of the courses and subjects must have a maximum of 10 letters
22. Courses can have the same names if they are from different units
23. ~~The student can only enroll in one course~~
24. The coordinator can coordinate more than one course
25. The coordinator can list the students, subjects and grades, and credits of all your courses (coordinator of more than one course)
26. The course can be canceled
27. Canceled courses cannot accept student applications
28. Canceled courses cannot have coordinators
29. Each subject can have a maximum of 30 students enrolled
30. ~~The student must enroll in at least 3 subjects~~
31. If the number of missing subjects of a student is less than 3, he can enroll in 1 subject
32. If the student does not enroll in the minimum number of subjects per semester, he will automatically fail
33. The student must have a CPF validated in the external CPF validation system (government system)
34. Add the name of the course in the coordinators' reports
35. The Student is only approved if he obtains the minimum grade in all subjects of the course, even if his credit is above the minimum
36. User must be able to create students with basic information
37. User must be able to enroll student in a course
38. The user must be able to create courses with the minimum number of subjects
39. The admin and only the admin should be able to list all students with detailed information (all available information)
40. The administrator and only the administrator must be able to list all courses with all available information
41. The administrator and only he must be able to list the list of students by course
42. The administrator and only he should be able to list the list of subjects per student
43. The student must be able to list all the subjects of his course only
44. The student must be able to list all of the subjects studied
45. The student must be able to list the missing materials
46. ​​The administrator should be able to list all course coordinators with available informationop
47. The student has 10 semesters to graduate
48. If the student exceeds 10 semesters, he is automatically failed
49. The coordinator can only be the coordinator of a maximum of 3 courses
50. The general coordinator cannot be a course coordinator