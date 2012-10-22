#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2011 Courgette
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
import threading, Queue
import urllib2 
import b3.plugin
from b3.events import EVT_CLIENT_AUTH, EVT_STOP

__version__ = '1.0'
__author__  = 'Courgette'



from xml.parsers.expat import ExpatError
try:
    from b3.lib.elementtree import ElementTree
except ImportError, err:
    from xml.etree import ElementTree

USER_AGENT =  "B3 VACban plugin/%s" % __version__
SERVICE_URL = "http://steamcommunity.com/profiles/"

SUPPORTED_PARSERS = ['homefront', 'ravaged']

#--------------------------------------------------------------------------------------------------
class VacbanPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    _workerThread = None # thread consumming the _checkqueue
    _checkqueue = Queue.Queue() # Queue containing Client objects to check against Valve AntiCheat webservice
    _checkqueue_end_token = object() # special token to put into _checkqueue to tell the _workerThread to stop
    _message_method = None


    def onLoadConfig(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self._getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        # load preferences
        self.load_config_preferences()


    def onStartup(self):
        if self.console.gameName not in SUPPORTED_PARSERS:
            self.error("This game is not supported by this plugin")
            self.disable()
            return
        self.registerEvent(EVT_CLIENT_AUTH)
        self._workerThread = threading.Thread(target=self._worker)
        self._workerThread.setDaemon(True)
        self._workerThread.start()
        self._checkConnectedPlayers()



    ###############################################################################################
    #
    #    config loaders
    #
    ###############################################################################################

    def load_config_preferences(self):
        self._message_method = self.debug
        try:
            msgtype = self.config.get('preferences', 'message_type')
            if msgtype.lower() == 'normal':
                self._message_method = self.console.say
                self.info("message_type is : normal")
            elif msgtype.lower() == 'big':
                self._message_method = self.console.saybig
                self.info("message_type is : big")
            else:
                self._message_method = self.info
                self.info("message_type is : none")
        except Exception, err:
            self.warning('cannot read preferences/message_type from config file (%s)', err)



    ###############################################################################################
    #
    #    event handlers
    #
    ###############################################################################################

    def onEvent(self, event):
        if event.type == EVT_CLIENT_AUTH:
            self._checkqueue.put(event.client)
        elif event.type == EVT_STOP:
            self.stop_worker()



    ###############################################################################################
    #
    #    commands
    #
    ###############################################################################################

    def cmd_vaccheck(self, data=None, client=None, cmd=None):
        """\
        check all players for VAC ban
        """
        if client is not None: client.message("checking players ...")
        self._checkConnectedPlayers()
        if client is not None: client.message("done")



    ###############################################################################################
    #
    #    Other methods
    #
    ###############################################################################################

    def _getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func
        return None


    def _checkConnectedPlayers(self):
        self.info("checking all connected players")
        clients = self.console.clients.getList()
        for c in clients:
            self._checkqueue.put(c)


    def _worker(self):
        while self.working:
            try:
                client = self._checkqueue.get(timeout=5)
            except Queue.Empty:
                continue
            if client == self._checkqueue_end_token:
                break
            self._checkClient(client)


    def stop_worker(self):
        self._checkqueue.put(self._checkqueue_end_token)

            
    def _checkClient(self, client):
        """\
        Examine players steam community id and allow/deny connection.
        """
        self.debug('checking %s (%s)', client, client.guid)
        try:
            response = self._query_service(client.guid)
        except Exception, err:
            self.exception(err)
        else:
            if response:
                try:
                    xml = ElementTree.XML(response)
                    error = xml.findtext('./error', None)
                    if error:
                        self.warning("Steam answered with error : %s", error)
                    else:
                        bandata = xml.findtext('./vacBanned', None)
                        if bandata is None:
                            self.info("cannot tell if banned. received : %s" % response)
                        elif bandata == '0':
                            self.info("%s has no VAC ban", client.name)
                        elif bandata == '1':
                            self.info("%s (%s) is banned by VAC", client.name, client.guid)
                            self._takeActionAgainst(client)
                except ExpatError, e:
                    self.error(e)
            else:
                self.warning("no response from VAC")


    def _query_service(self, uid):
        url = "%s/%s/?xml=1" % (SERVICE_URL.rstrip('/'), uid)
        self.info("querying %s", url)
        headers =  { 'User-Agent'  : USER_AGENT  }
        req =  urllib2.Request(url, None, headers)
        fp =  urllib2.urlopen(req)
        try:
            data = fp.read()
            return data
        except Exception, e:
            self.error(e)
        finally:
            fp.close()


    def _make_message_for(self, client):
        return self.getMessage('ban_message', self.console.getMessageVariables(self.console, client=client))


    def _takeActionAgainst(self, client):
        client.kick('VAC BANNED [%s]' % client.name, keyword="VACBAN", silent=True)
        try:
            msg = self._make_message_for(client)
            if msg and msg!="":
                self._message_method(msg)
        except b3.config.ConfigParser.NoOptionError, err:
            self.warning("could not find message ban_message in config file")




if __name__ == '__main__':

    from b3.fake import fakeConsole
    conf1 = b3.config.XmlConfigParser()
    conf1.loadFromString("""
    <configuration plugin="vacban">
        <settings name="commands">
            <!-- !vaccheck check all connected players against VAC -->
            <set name="vaccheck">100</set>
        </settings>
        <settings name="preferences">
            <!-- message_type defines how you want the ban message to be
            displayed on your game server :
                none : won't be displayed
                normal : normal chat message
                big : more noticeable message
            -->
            <set name="message_type">big</set>
        </settings>
        <settings name="messages">
            <!-- You can use the following keywords in your messages :
                $clientname
                $clientguid
            -->
            <!-- ban_message will be displayed to all players when a player is VAC banned -->
            <set name="ban_message">VACBAN $clientname ($clientguid)</set>
        </settings>
    </configuration>
    """)

    p = VacbanPlugin(fakeConsole, conf1)
    print(p._query_service("76561198011361489"))
    print(p._query_service("76561198016545586"))
    print(p._query_service("xxx"))

