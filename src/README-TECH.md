- Following the [Tutorial](https://fastapi.tiangolo.com/tutorial/) 
- Use python 3.11+
```bash
python -m venv venv
source venv/bin/activate
pip install "fastapi[standard]"
fastapi dev main.py
```
- Docs in http://localhost:8000/docs
- API in http://localhost:8000/

# CLI
```bash
python cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  info
  init-db
  list-db
  student
  teacher
```
## Example
```bash
python cli.py list-db

==== StudentDataManager NUIs ====
{'8292041704421': Student NUI 8292041704421 NAME ''}
{'8292041704257': Student NUI 8292041704257 NAME ''}
{'8292041705509': Student NUI 8292041705509 NAME ''}
{'8292041705541': Student NUI 8292041705541 NAME ''}
{'8292041705573': Student NUI 8292041705573 NAME ''}
{'8292041705609': Student NUI 8292041705609 NAME ''}
{'8292041705641': Student NUI 8292041705641 NAME ''}
{'8292041705673': Student NUI 8292041705673 NAME ''}
{'829204...
```