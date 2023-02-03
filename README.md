# Control of grades of college students
## Introduction
This project aims to exercise the "code smells" related to unit tests using an application that simulates a real business.
The code will be developed with the Detroit-style TDD technique, hence the name of the repository.
The application simulates the control of students' grades at a university. Below is the specification of the application:
Definition of Done:
1. Unit tests are covering the functionality
2. The functionality is designed to be used via CLI
3. Data is being saved to the database
# How to use
## Option 1: docker-compose
Run the commnands and access "http://localhost:5000"
```
chmod +x utils/build_container.sh
./utils/build_container.sh
./utils/build_dist.sh
docker-compose up -d
```
## Option 2: Kubernetes
Cosidering the Minikube and Virtual Box are installed, [Push the image](#publish-image) to Docker Hub and run the commands
```
minikube start --driver=virtualbox
```
### Declarative way
```
kubectl create -f kubernetes/deployments.yaml
kubectl create -f kubernetes/services.yaml
```

### Or Imperative way
```
kubectl create deployment tdd-detroid --image=douglasdcm/tdd-detroid
kubectl get pods
```
Create services
```
kubectl expose deployment tdd-detroid --type=NodePort --port=5000
kubectl get services
```
### Check access
```
curl $(minikube ip):<port>
```
and navigate to ```http://$(minikube ip):<port>```
## Option 3: locally by Live Server
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
## Option 4: locally by Flask
1. Run the commands above to setup the application
2. Start the aplication running the commnad bellow and access "http://localhost:5000"
```
python app.py
```
## Option 5: by CLI
5. It is possible to interact with the application using the command line. See more details in the help menu.
```
python cli. init-bd
python cli.py --help
```
# Config database for postgREST manually
```
python cli.py init-bd
docker exec -it postgres psql -U postgres
create schema api;

create role web_anon nologin;

grant usage on schema api to web_anon;
grant select on api.alunos to web_anon;
grant insert on api.alunos to web_anon;
grant delete on api.alunos to web_anon;

grant select on api.cursos to web_anon;
grant insert on api.cursos to web_anon;
grant delete on api.cursos to web_anon;

GRANT ALL ON TABLE api.alunos TO postgres;
GRANT ALL ON TABLE api.alunos TO web_anon;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA api TO web_anon;

create role authenticator noinherit login password 'mysecretpassword';
grant web_anon to authenticator;
```

# Technologies
This project uses pure Python in the backend, html for the screens, sqlite to store the records, PyScript to create the elements of the screens, Liver Server, docker-compose or kubernetes as options to bring the application up.
# Limitations
When used by the graphical interface, the inserted records are lost every time the screen is rendered. Persistence is only possible when used from the command line
# Publish image
Run the commands
```
docker login -u someuser -p somepassword
docker push douglasdcm/tdd-detroid:latest
```
# Notes about Kubernetes
```
app > docker/containerd > deployment() > k8s pod > k8s node > k8s cluster

if app down > k8s creats a new

if node down > k8s find other

* Notes

k8s pods: 1 or more containers

    https://kubernetes.io/docs/concepts/workloads/pods/

k8s node: virtual/phisical, has a container server to run pods

    https://kubernetes.io/docs/concepts/architecture/nodes/

k8s cluster: control plane/client [kubectl]
```
# Debug
Access a container in a pod
```
kubectl exec -it tdd-detroid-57fbdd679-4sj87 -c tdd-detroid bash
```
# Links
## K8s
Minikube: https://kubernetes.io/docs/tutorials/hello-minikube/<br>
Concepts: https://kubernetes.io/docs/concepts/architecture/<br>
API: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec<br>
Cluster Networking: https://kubernetes.io/docs/concepts/cluster-administration/networking/

## HTML
Attributes: https://www.w3schools.com/html/html_attributes.asp<br>
Tags: https://www.w3schools.com/tags/tag_pre.asp<br>
CSS: https://www.w3schools.com/css/css_howto.asp

## PyScript
Home: https://pyscript.net<br>
Issues: https://github.com/pyscript/pyscript/issues?q=websocket

## Pyodide
FAQ: https://pyodide.org/en/stable/usage/faq.html#how-can-i-send-a-python-object-from-my-server-to-pyodide

## PostgreSQL
Doc: https://docs.sqlalchemy.org/en/14/dialects/postgresql.html<br>
Doc: https://docs.sqlalchemy.org/en/14/core/pooling.html#pool-disconnects<br>
Erros: https://docs.sqlalchemy.org/en/14/errors.html#error-f405

## Websocket
Doc: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

## PostgREST
Home: https://postgrest.org/en/stable/<br>
Quick Start https://postgrest.org/en/stable/tutorials/tut0.html<br>
Operations: https://postgrest.org/en/stable/api.html#insertions

# Deliveries
Construction of the basic functions of the system
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