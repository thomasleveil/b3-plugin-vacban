# -*- encoding: utf-8 -*-
from mock import  call, patch
from mockito import when, any as anything
from b3.config import CfgConfigParser
from tests import PluginTestCase, vac_response_not_banned
from vacban import VacbanPlugin


class Test_client_connects(PluginTestCase):

    def setUp(self):
        super(Test_client_connects, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[foo]""")
        self.p = VacbanPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        when(self.p)._checkConnectedPlayers().thenReturn()
        self.p.onStartup()
        when(self.p)._query_service(anything()).thenReturn(vac_response_not_banned)


    def test_player_connects(self):
        # GIVEN
        with patch.object(self.p, '_checkClient') as mock_checkClient:
            # WHEN
            self.joe.connects("slot1")
            self.p.stop_worker()
            self.p._workerThread.join()
        # THEN
        mock_checkClient.assert_has_calls([
            call(self.joe)
        ])
        self.assertEqual(1, mock_checkClient.call_count)



    def test_2_players_connect(self):
        # GIVEN
        with patch.object(self.p, '_checkClient') as mock_checkClient:
            # WHEN
            self.joe.connects("slot1")
            self.simon.connects("slot2")
            self.p.stop_worker()
            self.p._workerThread.join()
            # THEN
        mock_checkClient.assert_has_calls([
            call(self.joe),
            call(self.simon)
        ])
        self.assertEqual(2, mock_checkClient.call_count)

