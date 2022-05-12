from django.test import TestCase

from compman import services as svc
from disciplines import GOMOKU
from compman.models import Table
from compman.tests import given


class TestTableService(TestCase):

    def test_propose_game(self):
        the_player = given.registered_player("Wolfie")

        the_table = svc.propose_game(GOMOKU, {'table_size': 15}, the_player)

        self.then_player_should_be_seated(the_table, the_player)

    def then_player_should_be_seated(self, table: Table, player):
        self.assertEqual(table.first_player, player)

    def test_move(self):
        wolfie = given.registered_player("Wolfie")
        harry = given.registered_player("Harry")
        table = svc.propose_game(GOMOKU, {'board_size': 15}, wolfie)
        table = svc.join_table(table, harry)
        svc.make_move(table, wolfie, "H8")
        self.assertEquals(table.state, "H8")
        self.assertEquals(table.last_move, "H8")
        self.assertEquals(table.prev_state, "")
        self.assertEquals(table.current_player, harry)

        svc.make_move(table, harry, 'G9')
        self.assertEquals(table.state, "H8G9")
        self.assertEquals(table.last_move, "G9")
        self.assertEquals(table.prev_state, "H8")
        self.assertEquals(table.current_player, wolfie)
