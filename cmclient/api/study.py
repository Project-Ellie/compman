from cmclient.api.basics import CompManConfig
from cmclient.gui import board


class StudyHandler:

    def __init__(self, config: CompManConfig):
        self.config = config
        self.current_state = ""

    def handle(self, args):
        self.study()

    def study(self):
        ret = board.show(registered="Self-Play Study", oppenent="", state="",
                         move_listener=lambda move: self.move(*move),
                         polling_listener=None)

    def move(self, x, y):
        move = f"{x}{y}"
        self.current_state += move
        return move
