# set -x
rm university.db
python for_admin.py
python cli.py enroll-student --name douglas --cpf 098.765.432.12 --course-name mat # 25a5a5c24a5252968097e5d5c80e6352
python cli.py take-subject --student-identifier 25a5a5c24a5252968097e5d5c80e6352 --subject-name calculus
python cli.py take-subject --student-identifier 25a5a5c24a5252968097e5d5c80e6352 --subject-name geometry
python cli.py update-grade --student-identifier 25a5a5c24a5252968097e5d5c80e6352 --subject-name calculus --grade 7
python cli.py update-grade --student-identifier 25a5a5c24a5252968097e5d5c80e6352 --subject-name geometry --grade 9
python cli.py calculate-gpa --student-identifier 25a5a5c24a5252968097e5d5c80e6352
python cli.py lock-course --student-identifier 25a5a5c24a5252968097e5d5c80e6352
python cli.py unlock-course --student-identifier 25a5a5c24a5252968097e5d5c80e6352

python cli.py enroll-student --name maria --cpf 028.745.462.18 --course-name mat
# python cli.py enroll-student --name aline --cpf 028.745.462.18 --course-name adm
python cli.py list-students --course-name mat

python cli.py remove-subject --course-name adm --subject-name management
python cli.py activate-course --name deact
python cli.py deactivate-course --name act
python cli.py cancel-course --name adm
python cli.py create-course --name geography --max-enrollment 11
python cli.py add-subject --course-name geography --subject-name minerals

python cli.py close-semester --identifier 2024-1
python cli.py list-courses