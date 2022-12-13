echo "Preparing the project to be pushed to remote repository"
# update requirements
pip freeze > requirements.txt
# report the status of git
git status
# execute the validatation
coverage run --include='app.py' --source='src' -m pytest -vvv -s
coverage report
coverage html
echo "Pre-commit finished"

