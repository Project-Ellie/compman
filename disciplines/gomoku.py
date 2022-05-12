INITIAL_STATE_REP = ["", "", ""]


class Board:

    def __init__(self, params, prev_state, last_move, state, current_player, history):
        self.current_player = current_player
        self.params = params
        self.prev_state = prev_state
        self.last_move = last_move
        self.state = state
        self.history = history

    def make_move(self, move: str):
        self.last_move = move
        self.prev_state = self.state
        self.state = self.state + move
        self.history.append(move)
        self.current_player = 1 - self.current_player
