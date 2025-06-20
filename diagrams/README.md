It is necessary to install `draw.io` extension to edit the files

# **Phase 1: Requirements Analysis & Scope Definition**  
1. **Elicit Functional Requirements**  
- Core entities: represent the main `nouns` present in the requirements
- States: represents the state for each core entity
- Actions: represent the actions each entity can do or suffer

## Missing requiements mapped during the code analysis
- Subject does not have a minimum students: found while implementing the state machine of the Course. In the `SequenceCore diagram` the Subject notifies the Course when it reaches the minimum number of students. The value was set to 3
- The minimun number of students per Course can not be 100: found while validating the state transation of the Course to InProgress. The minimum number of Subjects is 3 and each one need to have at least 3 students, so the minimun number of students to a course should be 9
- Teacher basic information not set: found during improving the logging to show the Teacher added to a Subject. The Teacher does not have name, id or other basic information. Added on-demand
- Teacher can set grade to locked Subject: found while reviwing the SequenceDiagram. Added a restriction to let the Teacher set grades just for Subjects with state 'in progress'

## Core Entities
### Administrator
#### Actions
- list all Students
- list all Courses
- list Student per Course
- list Subjects per Student
- list all Course Coordinator 


### Coordinator
#### State
- do not coordinate Courses
- coordinate less than the maximum Courses
- coordinate maximum Courses,
- coordinates more tham the maximum value of Courses
#### Actions
- coordinate
- list students of their Courses
- list subjects of their Courses
- list grades of their Courses
- list GPA of their Courses
- authenticate

### Coordinator's Report
### Course
#### State
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

### Course Coordinator
#### Actions
- list students
- list grades of Subjects
- list GPA of Students
- remove Subjects
- accept Student
- do not accept Student-
- add Subject to their Course

### Course Unique Identifier
### External CPF validation Sytem (Government System)
### Enrollment List
### General Coordinator
#### State
- is coordinator of Course (forbiden)
- is not Coordinator of Course

#### Actions
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

### Grade Control (GPA) (Grade?)
#### State
- under minimum value
- between minimum and maximum values
- above maximum value
- can update
- can not upate

### Semester
### Student
#### State
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
#### Actions
- lock the Course
- update Grades
- enroll in Course
- create Student
- list all their Subjects by Course
- list all taken Subjects
- (do not) take Subject?
- list missing Subjects
- authenticate

### Student Grade
### Student Credential
### Student History

### Subject
#### State
- can update
- can not update
- has minimum enrolled Students
- does not have minimum enrolled Students
- has enrolled Students over the maximum value
- locked
- unlocked

### Subject Unique Identifier
### Student's Situation
### Student Documentation
### System
### Units

### University
#### State
- does not have Courses
- does not have Subcjets
- has maximum Courses
- has maximum Subjects
- does not have maximum Courses
- does not have maximum Subjects 

### Teacher
#### Actions
- set the Grade of Students in their Subject
- teach maximum Subject
- does not teach maximum Subject
- authenticate

### Teacher Credential
### Coordinator Credential

2. **Non-Functional Requirements (NFRs)** 
No specific requirements. Just the authentication is necessary

3. **Prioritize with Stakeholders**
The core modules (Student, Teaching) are going to be developed first
## Deliverables
### Must Have
1. Each student will have a grade control called "grade point average" (GPA).
2. The GPA is the average of the student's grades in the ~~courses~~ subjects already taken.
3. The student is considered approved at the university if their GPA is above or equal to 7 (seven) at the end of the course.
4. If a student takes the same subject more than once, the highest grade will be considered in the GPA calculation.
5. Initially, the university will have 3 courses with 3 subjects each.
6. Subjects in each course may have the same names but will be differentiated by a unique identifier (niu).
7. The system must calculate the student's situation taking into account the subjects taken and the total number of subjects in each course.
8. The student can only take subjects from their course.
9. Courses must have a unique identifier and name.
12. The maximum grade for a student in a subject is 10.
13. The minimum grade for a student in a subject is 0.
14. The student can lock the course, and in this case, they cannot update their grades or the subjects taken.
16. The student can unlock the course, and their situation returns to the previous state.
17. Students must have names.
20. Students can only update their grades in the subjects they are enrolled in.
21. Course and subject names must have a maximum of 10 letters.
23. The student can only enroll in one course.
29. Each subject can have a maximum of 30 enrolled students.
30. The student must enroll in a minimum of 3 subjects.
31. If the number of subjects missing for a student is less than 3, they can enroll in 1 subject.
35. The students are only approved if they achieve the minimum grade in all course subjects, even if their GPA is above the minimum.
36. The ~~user~~ student (person) must be able to create students with basic information.
43. The students must be able to list all subjects only from their course.
44. The students must be able to list all subjects they have taken.
45. The students must be able to list the missing subjects.
51. The teacher sets thes grade for all students of his/her subjects
52. Each teacher may teach in 3 subjects at maximum

### Should Have
15.  The course coordinator can list the students, grades in each subject, and GPAs of the students.
18. The general coordinator can list all courses, students, grades in each subject, and GPAs of each student.
19. The course coordinator can remove subjects, and in this case, students cannot update their grades in that subject.
22. Courses can have the same names if they are from different units.
24. The coordinator can coordinate a maximum of three courses.
25. The coordinator can list the students, subjects, grades, and GPAs of all their courses (coordinator of more than one course).
26. The course can be canceled by the general cordinator.
27. Canceled courses cannot accept student enrollments.
28. Canceled courses cannot have coordinators.
34. Add the course name to the coordinator's reports.
33. The student must have a validated CPF (Brazilian Social Security Number) in the external CPF validation system (government system).
32. If the student does not enroll in the minimum number of subjects per semester, they will be automatically ~~failed~~ locked.
38. The ~~user~~ general coordinator must be able to create courses with the minimum number of subjects.
39. The administrator, and only the administrator, must be able to list all students with detailed information (all available information).
40. The administrator, and only the administrator, must be able to list all courses with all available information.
41. The administrator, and only the administrator, must be able to list the list of students per course.
42. The administrator, and only the administrator, must be able to list the list of subjects per student.
46. The administrator must be able to list all course coordinators with available information.
47. The student has 10 semesters to graduate.
48. If the student exceeds the 10 semesters, they are automatically failed.
50. The general coordinator cannot be a coordinator of courses.
53. The general coordinator is responsible to open and close the semesters
54. The general coordinator is responible to add students to enrollment list after manual analysis of thier documentation
55. The corse coordinator is responsible to add new subjects to his/her course
56. The general coordinator is responsible to add new courses to the university
57. The student, teacher and coordinators need to authenticate with valid credentials before perfom any action in the system
58. The course need a minimum enrollment of 100 students
59. The subject need a minimum enrollment of 10 students
60. Student can enroll to course again after fail it losing all his/her history


# **Phase 2: High-Level Architecture (HLA)**  

1. **Define Architectural Style**  
Layered: CLI (Presentation) -> Controller -> Business Logic -> Data. All in a monolitic system

2. **Component Diagram**
[Diagrams](./components.drawio)

3. **External Integrations**  
Integrated with fake components simulating the authenticator and the CPF validator

4. **Deployment View** 
No deployment. Will run locally in localhost

# **Phase 3: Mid-Level Design**  
1. **API Contracts**  
No REST API

2. **Data Flow Diagrams**  
[Diagrams](./components.drawio)

3. **Database Schema**
Not necessary. It will be used an in-memory database for simplicity

4. **State Transitions**  
[Diagrams](./components.drawio)

5. **Security Design**  
Just fake authentication

# **Phase 4: Low-Level Design (LLD)**  
1. **Class Diagrams**  
Check Phase1. Each Action will be mapped to a method  

2. **Algorithmic Logic**
Already in requirements and state diagrams


3. **Error Handling**  
Very permissive. No loggin

4. **Testability Hooks**  
Dependency injection of database
External components will be mocked

---

# **Phase 5: Cross-Cutting Concerns**  
1. **Logging**  
   Not applicable  

2. **Monitoring**  
    Not applicable  

3. **CI/CD Pipeline**  
    Not applicable

---

# **Phase 6: Validation & Feedback**  
*(Audience: Product Owners + Testers)*  

1. **Architecture Review**  
   - Walkthrough with developers (validate feasibility).  
   - Threat modeling (e.g., student impersonation attacks).  

2. **Prototyping**  
   - Spike: Implement auth flow + grade submission to test performance.  

3. **Documentation**  
   - HLA: C4 Model (Context, Containers, Components).  
   - LLD: Swagger for APIs, ER diagrams for DB.  