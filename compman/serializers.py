from rest_framework import serializers

from compman.models import Player, Table


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'discipline', 'first_player', 'second_player', 'current_player',
                  'params', 'prev_state', 'last_move', 'state']
