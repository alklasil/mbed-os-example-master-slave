**Usage:**

**Do beforehand**
1. set default interface to the interface to which the mbed network in connected to
  (for example ethernet)
  * The interface is not configurable as a commandline argument as of yet

**Command**
$ python main.py

**Gui**
 * "send" -> send message written in the textinput to the physical node
 * "more" -> show more options, information, ...

**Required**
Download Kivy: https://kivy.org/#home, https://kivy.org/#download

**Other**
The program works only on Linux OS + python2 for now.
  (Windows python socket cannot join group the same way Linux python can)
