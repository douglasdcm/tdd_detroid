clear
black -l 100 .
mypy .
flake8 --max-line-length 100
python -m pytest
