mkdir uml
pyreverse core -o png --project TDD --all-associated --colorized --all-ancestors --filter-mode ALL --output-directory uml --verbose --module-names y --show-stdlib
