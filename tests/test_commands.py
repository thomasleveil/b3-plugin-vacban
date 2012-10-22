# -*- encoding: utf-8 -*-
from mock import  patch
from mockito import when, any as anything
from b3.config import CfgConfigParser
from tests import PluginTestCase, vac_response_not_banned
from vacban import VacbanPlugin


class Test_commands(PluginTestCase):
    def setUp(self):
        super(Test_commands, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vaccheck: 20
        """)
        self.p = VacbanPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        when(self.p)._query_service(anything()).thenReturn(vac_response_not_banned)
        self.moderator.connects("2")



    def test_vaccheck(self):
        # GIVEN
        self.moderator.message_history = []
        # WHEN
        with patch.object(self.p, '_checkConnectedPlayers') as mock_checkConnectedPlayers:
            self.moderator.says("!vaccheck")
        # THEN
        self.assertEqual(['checking players ...', 'done'], self.moderator.message_history)
        self.assertEqual(1, mock_checkConnectedPlayers.call_count)
