from subprocess import PIPE, STDOUT, run

def executa_comando(argumentos):
    comando = ["python", "main.py"]
    comando.extend(argumentos)
    return run(comando,
                stdout=PIPE,
                stderr=STDOUT,
                text=True).stdout.strip()
