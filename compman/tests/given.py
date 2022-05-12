from compman.models import Player
from compman.services import register_player


def registered_player(name) -> Player:
    player_id = register_player(Player(name=name))
    return Player.objects.get(id=player_id)
