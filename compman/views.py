from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from compman.models import Player, Table
from compman.serializers import PlayerSerializer, TableSerializer

from compman import services
from compman.services import propose_game, join_table


def home_page_view(request):
    return HttpResponse("Hello, World!")


class TableViewSet(viewsets.GenericViewSet, RetrieveModelMixin):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        tables = Table.objects.all()
        serializer = self.get_serializer(instance=tables, many=True)
        return Response(data=serializer.data)

    @action(methods=['POST'], url_path='propose_game', detail=False)
    def propose_game(self, request, *args, **kwargs):
        params = request.data['params']
        player_id = request.data['player_id']
        discipline = request.data['discipline']
        the_player = Player.objects.get(id=player_id)
        table = propose_game(discipline=discipline, params=params, player=the_player)
        return Response(data={'table_id': table.id})

    @action(methods=['POST'], url_path='join_table', detail=False)
    def join_table(self, request, *args, **kwargs):
        table_id = request.data['table_id']
        player_id = request.data['player_id']
        the_player = Player.objects.get(id=player_id)
        the_table = Table.objects.get(id=table_id)
        the_table = join_table(the_table, the_player)
        data = TableSerializer(instance=the_table).data
        return Response(data=data)

    @action(methods=['POST'], url_path='clear', detail=False)
    def clear_all(self, request):
        Table.objects.all().delete()
        return Response(data={'message': 'OK.'})


class PlayerViewSet(viewsets.GenericViewSet, RetrieveModelMixin):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.all()

    def list(self, request, *args, **kwargs):
        players = Player.objects.all()
        serializer = self.get_serializer(instance=players, many=True)
        return Response(data=serializer.data)

    @action(methods=['POST'], url_path='register', detail=False)
    def register(self, request, **kwargs):
        serializer = PlayerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_player = Player(**data)
        services.register_player(new_player)
        return Response(data={'id': new_player.id})

    @action(methods=['POST'], url_path='clear', detail=False)
    def unregister_all(self, request):
        Player.objects.all().delete()
        return Response(data={'message': 'OK.'})


class GameViewSet(viewsets.GenericViewSet):

    def get_queryset(self):
        return Table.objects.all()

    @action(methods=['POST'], url_path='move', detail=False)
    def move(self, request, *args, **kwargs):
        x = request.data['x']
        y = request.data['y']
        player_id = request.data['player']
        table_id = request.data['table']

        table = Table.objects.get(id=table_id)
        player = Player.objects.get(id=player_id)
        if table.current_player != player:
            return Response(data={'result': "Not on you to move."},
                            status=status.HTTP_400_BAD_REQUEST)
        board = table.get_board()
        board.make_move(x+str(y))
        table.update_from_board(board)
        data = TableSerializer(instance=table).data
        return Response(data=data)
