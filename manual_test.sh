set -x
python cli.py enroll-student --name any --cpf 123.456.789-10 --course-identifier any
python cli.py enroll-student --name douglas --cpf 098.765.432.12 --course-identifier adm
python cli.py enroll-student --name any --cpf 123.456.789-10 --course-identifier invalid
python cli.py activate-course --name deact
