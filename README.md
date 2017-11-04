# 2017-arm-ohjelmistoprojekti

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


