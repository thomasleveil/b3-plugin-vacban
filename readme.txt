VAC ban plugin for Big Brother Bot (www.bigbrotherbot.net)
==========================================================

By Courgette


Description
-----------

For each connecting player, check if his steam community id is banned by VAC (any game)
Works only for games providing Steam community IDs



Installation
------------

 * copy vacban.py into b3/extplugins
 * copy plugin_vacban.xml into b3/extplugins/conf
 * update your main b3 config file with :

<plugin name="vacban" config="@b3/extplugins/conf/plugin_vacban.xml"/>



Changelog
---------

2011-04-25 - 0.1
* first release
2011-04-26 - 0.2
* fix issue when on client auth event
2011-04-26 - 0.3
* check game compatibility on startup


Support
-------

http://forum.bigbrotherbot.net/plugins-by-courgette/vac-ban-plugin
