class IState:
    def get_next_state(self, context) -> "IState":
        raise NotImplementedError
