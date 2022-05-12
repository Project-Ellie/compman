from django.db import models
import uuid
from disciplines import gomoku, GOMOKU


class BaseModel(models.Model):

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Player(BaseModel):

    def __str__(self):
        return f"Player '{self.name}'"

    __repr__ = __str__

    name = models.CharField(max_length=32)


BOARDS = {
    GOMOKU: gomoku.Board
}


class Table(BaseModel):

    def __str__(self):
        return f"Table ({self.discipline}) - id: {self.id}"

    __repr__ = __str__

    discipline = models.CharField(max_length=32)
    first_player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True, related_name='+')
    second_player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True, related_name='+')
    current_player = models.ForeignKey(to=Player, on_delete=models.CASCADE, null=True, related_name='+')
    params = models.JSONField(null=True)
    prev_state = models.CharField(max_length=4096, null=True)
    last_move = models.CharField(max_length=32, null=True)
    state = models.CharField(max_length=4096, null=True)
    history = models.JSONField(null=True)

    def get_board(self):
        constructor = BOARDS[self.discipline]
        current_player = 1 if self.second_player == self.current_player else 0
        return constructor(self.params, self.prev_state, self.last_move,
                           self.state, current_player, self.history)

    def update_from_board(self, board):
        self.prev_state = board.prev_state
        self.last_move = board.last_move
        self.state = board.state
        self.history = board.history
        self.current_player = self.first_player if board.current_player == 0 else self.second_player
        self.save()
