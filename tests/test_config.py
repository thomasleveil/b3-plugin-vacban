# -*- encoding: utf-8 -*-
import logging
from b3.config import CfgConfigParser
from tests import PluginTestCase
from vacban import VacbanPlugin


class Test_config(PluginTestCase):

    def setUp(self):
        super(Test_config, self).setUp()
        self.conf = CfgConfigParser()
        self.p = VacbanPlugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.INFO)

    def tearDown(self):
        self.p.stop_worker()


    def test_empty_config(self):
        self.conf.loadFromString("""
[foo]
        """)
        self.p.onLoadConfig()
        # should not raise any error


    #-------------------- load_config_preferences ------------------------

    def test_load_config_preferences__message_type__normal(self):
        # GIVEN
        self.conf.loadFromString("""
[preferences]
message_type: normal
        """)
        # WHEN
        self.p.load_config_preferences()
        # THEN
        self.assertEqual(self.console.say, self.p._message_method)


    def test_load_config_preferences__message_type__big(self):
        # GIVEN
        self.conf.loadFromString("""
[preferences]
message_type: big
        """)
        # WHEN
        self.p.load_config_preferences()
        # THEN
        self.assertEqual(self.console.saybig, self.p._message_method)


    def test_load_config_preferences__message_type__empty(self):
        # GIVEN
        self.conf.loadFromString("""
[preferences]
message_type:
        """)
        # WHEN
        self.p.load_config_preferences()
        # THEN
        self.assertEqual(self.p.info, self.p._message_method)


    def test_load_config_preferences__message_type__f00(self):
        # GIVEN
        self.conf.loadFromString("""
[preferences]
message_type: f00
        """)
        # WHEN
        self.p.load_config_preferences()
        # THEN
        self.assertEqual(self.p.info, self.p._message_method)



    #-------------------- load_config_preferences ------------------------

    def test_messages__ban_message(self):
        # GIVEN
        self.conf.loadFromString("""
[messages]
; You can use the following keywords in your messages :
;   $clientname
;   $clientguid

;ban_message will be displayed to all players when a player is VAC banned
ban_message: VACBAN $clientname ($clientguid) f00
        """)
        # WHEN
        msg = self.p._make_message_for(self.joe)
        # THEN
        self.assertEqual("VACBAN Joe (joe_guid) f00", msg)
