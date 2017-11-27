#### **Usage:**

**Steps before starting program**
1. set default interface to the interface to which the mbed network in connected to
  (for example ethernet)
  * The interface is not configurable as a commandline argument as of yet

**Command**
$ python main.py

**Gui**
 * "send" -> send message written in the textinput to the physical node
 * "more" -> show more options, information, ...

Currently you configure the nodes using this interface, by assigning each node discovered in
in the network one or multiple slave groups, one or multiple master groups or many of both.
You type the command as 
"conf;g1,g2,g3,g4;g4,g5,g6;"
To assign it to the master groups 1,2,3,4 and slave groups 4,5,6.

**Required**
Download Kivy: https://kivy.org/#home, https://kivy.org/#download

**Other**
The program works only on Linux OS + python2 for now.
  (Windows python socket cannot join group the same way Linux python can)
