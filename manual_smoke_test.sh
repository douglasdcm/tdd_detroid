# set -x
rm university.db
python for_admin.py
python cli.py enroll-student --name any --cpf 123.456.789-10 --course-name any
python cli.py take-subject --student-identifier 290f2113c2e6579c8bb6ec395ea56572 --subject-name any1
python cli.py take-subject --student-identifier 290f2113c2e6579c8bb6ec395ea56572 --subject-name any2
python cli.py update-grade --student-identifier 290f2113c2e6579c8bb6ec395ea56572 --subject-name any1 --grade 7
python cli.py update-grade --student-identifier 290f2113c2e6579c8bb6ec395ea56572 --subject-name any2 --grade 9
python cli.py calculate-student-gpa --student-identifier 290f2113c2e6579c8bb6ec395ea56572

python cli.py activate-course --name deact
python cli.py deactivate-course --name act
python cli.py cancel-course --name any