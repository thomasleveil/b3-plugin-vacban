import unittest
import logging
from mockito import when
from b3.config import XmlConfigParser
from b3.fake import FakeConsole, FakeClient
from b3.plugins.admin import AdminPlugin


class DummyParser(FakeConsole):
    gameName = "ravaged"


class PluginTestCase(unittest.TestCase):

    def setUp(self):
        # less logging
        logging.getLogger('output').setLevel(logging.ERROR)

        # create a parser
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString("""<configuration></configuration>""")
        self.console = DummyParser(self.parser_conf)
        self.console.startup()

        # load the admin plugin
        self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.xml')
        self.adminPlugin.onStartup()

        # make sure the admin plugin obtained by other plugins is our admin plugin
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)


        # prepare a few players
        self.joe = FakeClient(self.console, name="Joe", guid="joe_guid", groupBits=1)
        self.simon = FakeClient(self.console, name="Simon", guid="simon_guid", groupBits=0)
        self.moderator = FakeClient(self.console, name="Moderator", guid="moderator_guid", groupBits=8)

        logging.getLogger('output').setLevel(logging.DEBUG)


    def tearDown(self):
        self.console.working = False




vac_response_banned = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<profile>
	<vacBanned>1</vacBanned>
</profile>
'''

vac_response_not_banned = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<profile>
	<vacBanned>0</vacBanned>
</profile>
'''

vac_response_not_found = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<response>
    <error><![CDATA[The specified profile could not be found.]]></error>
</response>
'''