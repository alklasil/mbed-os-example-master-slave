# 2017-arm-ohjelmistoprojekti

This is a prototype smart home IoT application that allows configuring a 
master-slave network using K64F development boards that runs on Arm Mbed OS.
The create 6lowPAN wireless mesh grid, where you can have boards configured as 
border routers, buttons and light nodes.

Setting up: In order to test this yourself, follow the setup guide to start the 
development found at https://os.mbed.com/getting-started/, and make sure the
"mbed" command is available on your path.

#### Compiling

When cloning the project, you can with two commands compile and load the project to a node.

**The mesh node** requires 2 commands:

"mbed deploy" and "mbed compile -t GCC_ARM -m K64F" 

which first downloads the mbed-os to the same folder where it's installed. Then you compile it using the selected toolchain and target board.
The toolchain used is the ARM_GCC, which is found at https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads

Once you have it compiled, copy the <folder name>.bin file in to the portable device (board) that is connected to your computer. It will automatically be written to the board, and start running.
 
 **The border router** also requires 2 commands

TODO


#### Usage

The python server requires python to be installed on your system, as well as the kivy framework. https://kivy.org/#download
It's a simple framework that allows for creating simple user interfaces.

It runs with the command "python main.py", and attaches itself to the default web interface. 
Make sure you have ethernet plugged in to the border router, it listens to the mesh network 
through the border router.

Currently you configure the nodes using this interface, by assigning each node discovered in
in the network one or multiple slave groups, one or multiple master groups or many of both.
You type the command as 
"conf;g1,g2,g3,g4;g4,g5,g6;"
To assign it to the master groups 1,2,3,4 and slave groups 4,5,6.

You can also configure every node at once.

**REQUIREMENTS**


**_Requirements for User Interface_**

* [x] Joins a multicast group address which is defined for the demo.
* [x] Listens for incoming advertisements from nodes.
* [x] (~list) Displays a list of found nodes for user, separate by function (button/switch, light)
  * **TODO:** possibility for displaying the nodes as a list (separated by node_mode)
* [x] Allows user to create connection between a button and a light.
  * **TODO:** make simplier
* [x] When creating connection, send a unicast message for node telling which button to listen to.

**_Requirements for Node applications_**

* Node may refer to a button or a lighting node which both contain very similar software.
  * Only advertise message is different at the moment

* [x] Application connects to 6LoWPAN-ND based network
* [x] Application receives IPv6 address from network
* [x] Once connected node joins to a specified multicast group
* [x] Node listens for UDP messages on port 1030

**_Requirements for Light node_**

* This is a node which contains a light bulb or LED connected to it.

* [x] When receiving a controlling message from the user interface, records the address which this node should listen to for incoming switch commands.
  * At the moment address ≃ group_id, it's stupid to use addresses as they only waste bytes
* [x] When receiving a multicasted message from a button node, compares the source address to one received from UI. If matches, switches the light.
  * address ≃ group_id

* HOX! You can configure a button to send its own address as the master_group id
           and configure a light to listen to that same address
    -> works as if the light listened for only certain addresses and responded to them

