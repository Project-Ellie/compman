from unittest import TestCase

from cmclient.api.basics import CompManConfig
from cmclient.api.study import StudyHandler


class TestStudyHandler(TestCase):

    def test_lifecycle(self):
        config = CompManConfig("", "", "")
        handler = StudyHandler(config)
        handler.handle(config)

