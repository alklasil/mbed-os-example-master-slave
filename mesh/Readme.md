Usage (at the moment):
  * follow instructions in the following page: https://github.com/ARMmbed/mbed-os-example-mesh-minimal
  * when the mbed-os-example-mesh-minimal is working:
    * copy and paste the files in the mbed-os-example-mesh-minimal repo into this folder (do not replace the existing files, only copy the files that do not already exist) <or act otherwise more or less similarly>
  
**message format:**

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
  
 
