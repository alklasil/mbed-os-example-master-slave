Usage (at the moment):
  * This project is based on the "Example mesh application for mbed OS" (https://github.com/ARMmbed/mbed-os-example-mesh-minimal)
  * This folder contains the modified versions of the files used in the above project.
  
**message format:**

The node deals with 3 different kinds of messages:
  * (1) messages that the nodes do not need to care about (such as advertise to the backhaul network)
  * (2) control messages (such as light control messages)
    * when a node receives a control message, it checks whether the sender is its master
    * if the sender is a master, the receiver acts according to the control message, otherwise the receiver ignores the control message
  * (3) configuration messages (such as setting master_buffer and slave_buffer):
    * when a node receives this kind of message, it configures itself according to the instructions
    * (at the moment any single node can configure any single node (or all nodes) without requiring authentication [at least at the moment])
    * for now the UI uses these messages to configure the nodes to listen/send to only certain nodes (certain groups).
  
**More information and examples**

* Advertise: "#advertise:mode;s:%d;", state
  * for example: "#advertise:button;s:%d;", state
* light control: "%s;t:lights;s:?;", master_buffer ? master_buffer : "g"
  * for example: "group1;t:lights;s:?;"
* configuration: "conf;slave_buffer;master_buffer"
  * format(slave_buffer) == format(master_buffer) = "group1,grup2,grup3,...,groupN;"
  * for example: 
    *node1: "conf;hall,bedroom;hall,upstairs;"
    *node2: "conf;upstairs;;"
    *node3: "conf;mount_everest;moon;"
    -> node1 sends message to its master groups:
      -> e.g., light control message gets send to the groups "hall" and "upstairs"
    -> nodes in the network (including the sender) listen messages to the groups they are slaves in:
      -> e.g., node1 itself belongs to the "hall" group and thus switches its state
      ->       node2 belongs to the "upstairs" group and thus switches its state
      ->       node3 receives the message but does not belong to any of the groups the message was sent to and thus nodes not change state
                  (not slave_groups(node3) in master_groups(node2))
  
 
