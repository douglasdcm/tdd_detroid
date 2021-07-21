from subprocess import PIPE, STDOUT, run
from src.config import ponto_entrada


def executa_comando(argumentos):
    try:
        comando = ["python", ponto_entrada]
        comando.extend(argumentos)
        return run(comando,
                   stdout=PIPE,
                   stderr=STDOUT,
                   encoding="utf-8").stdout.strip()
    except Exception:
        raise
