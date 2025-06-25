"""Interface to define all Concrete States"""


class IState:
    @staticmethod
    def get_next_state(context) -> "IState":
        raise NotImplementedError
