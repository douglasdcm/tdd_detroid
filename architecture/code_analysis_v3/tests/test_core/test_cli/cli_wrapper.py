from core.custom_logger import spy_logger
from tests.test_core.test_cli.linux_terminal import LinuxTerminal


class StudentCli(LinuxTerminal):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    @spy_logger
    def add_info(self, nui, name, age):
        self.run(f"python cli.py student add-info --nui {nui} --name {name} --age {age}")

    @spy_logger
    def subscribe(self, nui, snui):
        self.run(f"python cli.py student subscribe --nui {nui} --snui {snui}")

    @spy_logger
    def list_subjects(self, nui):
        return self.run(f"python cli.py student list-subjects --nui {nui}")

    @spy_logger
    def list_information(self, nui):
        return self.run(f"python cli.py student list-info --nui {nui}")


class TeacherCli(LinuxTerminal):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    @spy_logger
    def add_info(self, nui, name, age):
        self.run(f"python cli.py teacher add-info --nui {nui} --name {name} --age {age}")

    @spy_logger
    def subscribe(self, nui, snui):
        self.run(f"python cli.py teacher subscribe --nui {nui} --snui {snui}")

    @spy_logger
    def list_subjects(self, nui):
        return self.run(f"python cli.py teacher list-subjects --nui {nui}")

    @spy_logger
    def list_information(self, nui):
        return self.run(f"python cli.py teacher list-info --nui {nui}")
