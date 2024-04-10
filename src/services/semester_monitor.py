import uuid
import datetime


class SemesterHandler:
    def __init__(self) -> None:
        self.__identifier = "2024-1"  # TODO get next from database
        self.__state = "open"

    @property
    def identifier(self):
        return self.__identifier

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value
