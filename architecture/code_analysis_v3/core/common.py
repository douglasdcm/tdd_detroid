class IState:
    def __repr__(self):
        return f"{self.__class__.__name__}"

    def get_next_state(self, context) -> "IState":
        raise NotImplementedError
