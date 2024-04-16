# set -x
rm university.db
python for_admin.py
python cli.py enroll-student --name any --cpf 123.456.789-10 --course-name any
python cli.py enroll-student --name douglas --cpf 098.765.432.12 --course-name adm
python cli.py enroll-student --name any --cpf 123.456.789-10 --course-name invalid
python cli.py activate-course --name deact
python cli.py deactivate-course --name act
python cli.py cancel-course --name any
python cli.py calculate-student-gpa --student-identifier 290f2113c2e6579c8bb6ec395ea56572
