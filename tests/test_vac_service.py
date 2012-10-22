# -*- encoding: utf-8 -*-
from mock import  call, patch
from mockito import when, any as anything
from b3.config import CfgConfigParser
from tests import PluginTestCase, vac_response_not_banned, vac_response_banned, vac_response_not_found
from vacban import VacbanPlugin


class Test_vac_service(PluginTestCase):

    def setUp(self):
        PluginTestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = VacbanPlugin(self.console, self.conf)


    def test__checkClient__banned(self):
        # GIVEN
        when(self.p)._query_service(anything()).thenReturn(vac_response_banned)
        self.joe.connects("slot1")
        # WHEN
        with patch.object(self.p, "_takeActionAgainst") as mock_takeActionAgainst:
            self.p._checkClient(self.joe)
        # THEN
        mock_takeActionAgainst.assert_called_with(self.joe)
        self.assertEqual(1, mock_takeActionAgainst.call_count)


    def test__checkClient__not_banned(self):
        # GIVEN
        when(self.p)._query_service(anything()).thenReturn(vac_response_not_banned)
        self.joe.connects("slot1")
        # WHEN
        with patch.object(self.p, "_takeActionAgainst") as mock_takeActionAgainst:
            self.p._checkClient(self.joe)
        # THEN
        self.assertEqual(0, mock_takeActionAgainst.call_count)


    def test__checkClient__not_found(self):
        # GIVEN
        when(self.p)._query_service(anything()).thenReturn(vac_response_not_found)
        self.joe.connects("slot1")
        # WHEN
        with patch.object(self.p, "_takeActionAgainst") as mock_takeActionAgainst:
            self.p._checkClient(self.joe)
        # THEN
        self.assertEqual(0, mock_takeActionAgainst.call_count)



    def test__checkClient__error(self):
        # GIVEN
        when(self.p)._query_service(anything()).thenRaise(NotImplementedError('foo'))
        self.joe.connects("slot1")
        # WHEN
        with patch.object(self.p, "_takeActionAgainst") as mock_takeActionAgainst:
            self.p._checkClient(self.joe)
        # THEN
        self.assertEqual(0, mock_takeActionAgainst.call_count)


