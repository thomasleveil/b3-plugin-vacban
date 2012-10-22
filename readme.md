VAC ban plugin for Big Brother Bot (www.bigbrotherbot.net)
==========================================================

By Courgette


Description
-----------

For each connecting player, check if his steam community id is banned by VAC (any game)
Works only for games providing Steam community IDs



Installation
------------

 - copy vacban.py into 'b3\extplugins' folder
 - copy plugin_vacban.ini into your B3 'conf' folder (next to b3.xml)
 - update your main b3 config file with :

    ```
    <plugin name="vacban" config="@conf/plugin_vacban.ini" />
    ```


Changelog
---------

2011-04-25 - 0.1
- first release

2011-04-26 - 0.2
- fix issue when on client auth event

2011-04-26 - 0.3
- check game compatibility on startup

2012-10-22 - 1.0
- change: supports new game Ravaged
- change: config file is now a ini file
- change: do not block B3 when B3 is shutting down
- new: automated tests



Support
-------

http://forum.bigbrotherbot.net/plugins-by-courgette/vac-ban-plugin
