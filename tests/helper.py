import subprocess
from subprocess import PIPE, STDOUT, run

def executa_comando(comando):
    return subprocess.run(comando,
                    stdout=PIPE,
                    stderr=STDOUT,
                    text=True).stdout.strip()
