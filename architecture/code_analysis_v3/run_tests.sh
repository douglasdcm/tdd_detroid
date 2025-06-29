clear
black -l 100 .
flake8 --max-line-length 100
mypy .
python -m pytest -s
