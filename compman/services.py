from cmclient.api.basics import ValidationException
from compman.models import Player, Table
from disciplines.initial import INITIAL_STATE_REPS


def register_player(player: Player):
    player.save()

    return player.id


def propose_game(discipline: str, params: dict, player: Player):

    prev_state, last_move, state = INITIAL_STATE_REPS[discipline]

    table = Table.objects.create(discipline=discipline, first_player=player,
                                 current_player=player,
                                 params=params,
                                 prev_state=prev_state,
                                 last_move=last_move,
                                 state=state,
                                 history=[])
    return table


def join_table(table: Table, player: Player) -> Table:
    table.second_player = player
    table.current_player = table.first_player
    table.save()
    return table


def make_move(table: Table, player: Player, move: str):
    if player != table.current_player:
        raise ValidationException("Not your move, man!")
    board = table.get_board()
    board.make_move(move)
    table.update_from_board(board)
    table.save()
