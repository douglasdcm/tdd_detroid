import logging
import subprocess as s

from core.custom_logger import spy_logger


LOGGER = logging.getLogger(__name__)


class LinuxTerminal:
    def __repr__(self):
        return f"{self.__class__.__name__}"

    @spy_logger
    def run(self, command):
        LOGGER.info(f"Command {command}")
        out = s.run(command, text=True, shell=True, capture_output=True)
        if out.stderr:
            LOGGER.error(f"Command {command} Error '{out.stderr}'")
        return out.stdout

    @spy_logger
    def call(self, command):
        LOGGER.info(f"Command {command}")
        code = s.call(command, shell=True)
        if code != 0:
            LOGGER.error(f"Command failed with code {code}")
        return code
