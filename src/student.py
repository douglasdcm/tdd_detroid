class Student:
    def __init__(self):
        self.__score = 0

    def set_score(self, score):
        self.__score = score

    def get_score(self):
        return self.__score
