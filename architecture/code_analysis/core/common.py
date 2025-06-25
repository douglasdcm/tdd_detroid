class IState:
    def get_next_state(context) -> "IState":
        raise NotImplementedError
