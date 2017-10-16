Usage:

0. make sure default network interface is ethernet
1. cmd: python main.py (no additional parameters at the moment [add possibility to choose ethernet <and others> later])
2. double click -> send to node:
    * msg = 'conf;gs1,gs2;gm1,gm2'
      gs1,gs2 = what groups to listen for commands
      gm1,gm2 = what groups to send commands to

TODO:

* [ ] add comments
* [ ] clear code
* [ ] change image if old mode unknown and new mode other than unknown (+ node-mode named file exists) when advertise
* [ ] make is_active/running node outdated handling better, and show when node is outdated to the user in the ui
* [ ] resolve cached images related issue(s)
* [ ] other minor things
* Add Other TODOs in this list

