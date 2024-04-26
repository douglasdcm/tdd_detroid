{Translated from Portuguese to English using AI}
# College Student Grade Control
## Introduction
This project aims to practice architecture skills using an application that simulates a real business scenario.
The code will be developed using the TDD technique in the Detroit style, hence the name of the repository.
The application simulates the control of grades for university students.

# Architecture
[Slides with specifications (Libre Office file)](architecture.odp)

## Exploration
[2024-04-22] After a brief overview of the authetication systems listed in this [link](https://expertinsights.com/insights/top-10-user-authentication-and-access-management-solutions/) the two selected for exploration were [Duo Access](https://duo.com/docs/getting-started) and [Kinde](https://kinde.com/docs/developer-tools/python-sdk/) due the simplicity and the possibility to test them for free. Both provide a Python SDK. The only way to use the 2FA of Duo Access was by SMS. It is not clear if the service is charged or not. It works fine, but, when using the Demo App, at the end of the authenticaton process an error happened, so it was not possible to determine if the issue was in the configuration or in the system. Kinde also has a starter kit in GitHub. It worked fine too and the 2FA is provided by e-mail. Further investiation is going to be done with Kinde as it allows the 2FA by email.

References:
 - [Duo GitHub](https://github.com/duosecurity/duo_universal_python/tree/main/demo)
 - [Kinde GitHub](https://github.com/kinde-starter-kits/python-starter-kit)

[2024-04-24] The authnetication method chosen was Kinde. There is an [API documention](https://kinde.com/api/docs/?http#kinde-management-api-oauth) to it. We use the end-point "user_profile" and the token to check if the user is logged in. Other usefull links show how to test Kinde using Postman
  - https://www.youtube.com/watch?v=xJCj0IeoB5g
  - https://kinde.com/docs/build/get-access-token-for-connecting-securely-to-kindes-api/

While exploring it other options were found, but didn't fit the necessities of the project:
 - https://stackoverflow.com/questions/29625003/how-to-handle-user-authentication-for-a-cli-in-python-using-click
 - https://github.com/Zverik/cli-oauth2
 - https://auth0.com/blog/securing-a-python-cli-application-with-auth0/


# Setup and Test
```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest --random-order
```

# Installation
 - Need to create a new account in [Kinde](https://app.kinde.com/auth/cx/_:nav&m:register&psid:57419340529d47048c155f939bfcce4c) to use it.
 - Create a new Python application in Kinde, get the client_id, client_secret and domian (the name of the application)
 - Rename the file `config_template.py` to `config.py` and replace the Kinde data
 - Start the flask app

```
flask run
```
 - Access the home page (http://localhost:5000) and Sing Up a new user informing the email
 - Access to this email, copy the code sent by YOUR DOMAIN and fill the `Code` field in Sign Up page
 - The login should work
 - Go to Kinde and configure a role called "student" and other called "coordinator"
 - Assig the created user to both roles. Ideally each user has just one the roles, but for a simple setup it is fine to set both for the same user
 - Go back to Sign Up page and click the button "User Details" in Login page to get the token. Copy it.
 - Need to populate the database with allowed students, the courses and subjects.
```
python cli.py set-token # inform the token
./manual_smoke_test.sh
```

# CLI Usage
```
python cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  activate-course
  add-subject
  calculate-gpa
  cancel-course
  close-semester
  create-course
  deactivate-course
  enroll-to-course
  list-courses
  list-students
  lock-course
  remove-subject
  set-token
  take-subject
  unlock-course
  update-grade

# enroll student to course
python cli.py enroll-to-course --name douglas --cpf 098.765.432.12 --course-name mat

```

# Application specification

Below is the specification of the application:
Definition of Done:
1. Unit tests cover the functionality.
2. The functionality is developed to be used via CLI (Command Line Interface).
3. Data is being saved in the database.
# Deliverables
Construction of the basic functions of the system
1. **DONE** Each student will have a grade control called "grade point average" (GPA).
2. **DONE** The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.
3. **DONE** The student is considered approved at the university if their GPA is above or equal to 7 (seven) at the end of the course.
4. If a student takes the same subject more than once, the highest grade will be considered in the GPA calculation.
<!-- Required setup to allow enrollments -->
5. **DONE** Initially, the university will have 3 courses with 3 subjects each.
6. **DONE** Subjects in each course may have the same names but will be differentiated by a unique identifier (niu).
7. **DONE** The system must calculate the student's situation taking into account the subjects taken and the total number of subjects in each course.
8. **DONE** The student can only take subjects from their course.
9. **DONE** Courses must have a unique identifier and name.
<!-- 
Same as requirement 6
10. ~~Course~~ Subject names can be the same, but the unique identifier for each ~~course~~ subject must be different. -->
<!-- 
Same as requirement 6
11. A course cannot have two subjects with the same name, even if the niu is different. -->
12. **DONE** The maximum grade for a student in a subject is 10.
13. **DONE** The minimum grade for a student in a subject is 0.
14. **DONE** The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
15. **DONE**  The course coordinator can list the students, grades in each subject, and GPAs of the students.
16. **DONE** The student can unlock the course, and their situation returns to the previous state.
17. **DONE** Students must have names.
18. **DONE** The general coordinator can list all courses, students, grades in each subject, and GPAs of each student.
19. **DONE** The course coordinator can remove subjects, and in this case, students cannot update their grades in that subject.
20. **DONE** Students can only update their grades in the subjects they are enrolled in.
21. **DONE** Course and subject names must have a maximum of 10 letters.
<!-- What are units? Not clear -->
22. Courses can have the same names if they are from different units.
<!-- The student can do it any time. Don't need to wait the next semester -->
23. **DONE** The student can only enroll in one course.
24. The coordinator can coordinate a maximum of three courses.
25. **DONE** The coordinator can list the students, subjects, grades, and GPAs of all their courses (coordinator of more than one course).
<!-- this requirement wasn't informing the actor. Figured out while making the diagrams of use cases -->
<!-- 26. The course can be canceled. -->
26. **DONE** The course can be canceled by the general cordinator.
27. **DONE** Canceled courses cannot accept student enrollments.
<!-- How o set coordinators? -->
28. Canceled courses cannot have coordinators.
29. **DONE** Each subject can have a maximum of 30 enrolled students.
<!-- ... 3 subjects per semester -->
30. The student must enroll in a minimum of 3 subjects.
31. If the number of subjects missing for a student is less than 3, they can enroll in 1 subject.
32. If the student does not enroll in the minimum number of subjects per semester, they will be automatically ~~failed~~ locked.
33. **DONE** The student must have a validated CPF (Brazilian Social Security Number) in the external CPF validation system (government system).
34. **DONE** Add the course name to the coordinator's reports.
35. **DONE** The students are only approved if they achieve the minimum grade in all course subjects, even if their GPA is above the minimum.
<!-- The user can create student with cpf and name. Considering DONE -->
36. **DONE** The ~~user~~ student (person) must be able to create students with basic information.
<!-- The basic information is enough for enrollment -->
37. ~~The user must be able to enroll the student in a course.~~
38. **DONE** The ~~user~~ general coordinator must be able to create courses with the minimum number of subjects.
39. The administrator, and only the administrator, must be able to list all students with detailed information (all available information).
40. The administrator, and only the administrator, must be able to list all courses with all available information.
41. The administrator, and only the administrator, must be able to list the list of students per course.
42. The administrator, and only the administrator, must be able to list the list of subjects per student.
43. The students must be able to list all subjects only from their course.
44. The students must be able to list all subjects they have taken.
45. The students must be able to list the missing subjects.
<!-- The course coordinator is not an entity yet. What are his/her properties? -->
46. The administrator must be able to list all course coordinators with available information.
47. **DONE** The student has 10 semesters to graduate.
48. **DONE** If the student exceeds the 10 semesters, they are automatically failed.
<!-- Duplicated with requirement 24 -->
49. ~~The coordinator can only coordinate a maximum of 3 courses~~.
50. The general coordinator cannot be a coordinator of courses.
<!-- # Features add after architecture analisys
These features were introduced after analysis in architecture and specifications. Some features does not make sense without them: -->
51. The teacher sets thes grade for all students of his/her subjects
52. Each teacher may teach in 3 subjects at maximum
53. The general coordinator is responsible to open and close the semesters
54. The general coordinator is responible to add students to enrollment list after manual analysis of thier documentation
55. The corse coordinator is responsible to add new subjects to his/her course
56. The general coordinator is responsible to add new courses to the university
57. The student, teacher and coordinators need to authenticate with valid credentials before perfom any action in the system
58. The course need a minimum enrollment of 100 students
59. The subject need a minimum enrollment of 10 students
60. Student can enroll to course again after fail it losing all his/her history
