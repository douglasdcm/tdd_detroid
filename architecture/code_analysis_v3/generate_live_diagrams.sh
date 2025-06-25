mypy .
mkdir uml
pyreverse core cli.py -o png --project TDD --all-associated --colorized --all-ancestors --filter-mode ALL --output-directory uml --verbose --module-names y --show-stdlib --ignore exceptions.py,base_object.py,common.py
