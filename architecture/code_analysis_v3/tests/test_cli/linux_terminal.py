import subprocess as s

from core.spy_logger import spy_logger


"""Performs commands on Linux Terminal"""


class LinuxTerminal:
    def __repr__(self):
        return f"{self.__class__.__name__}"

    @spy_logger
    def run(self, command):
        print(command)
        out = s.run(command, shell=True, capture_output=True)
        if out.stderr:
            print(out.stderr.decode())
        return out.stdout.decode("utf-8")

    @spy_logger
    def call(self, command):
        print(command)
        code = s.call(command, shell=True)
        if code != 0:
            print(f"Command failed with code {code}")
        return code
