# Mesh-node

This is based on [mbed-os-example-mesh-minimal](https://github.com/ARMmbed/mbed-os-example-mesh-minimal)

### Download the application

* This folder contains all the required files for compiling the application.
* You can either clone the repo or download the zip.

### [Compile the application](https://github.com/ARMmbed/mbed-os-example-mesh-minimal#compile-the-application)

#### [Default configuration](https://github.com/alklasil/2017-arm-ohjelmistoprojekti/tree/documentation-update#required)

```
mbed deploy
mbed compile
```

* To modify the configuration, follow the instructions given in [mbed-os-example-mesh-minimal](https://github.com/ARMmbed/mbed-os-example-mesh-minimal).

#### [Program the target](https://github.com/ARMmbed/mbed-os-example-mesh-minimal#program-the-target)

Drag and drop the binary to the target to program the application.


### Specifications

#### Common
* A running node listens for unicast and multicast udp messages.
* A running node sends multicast udp messages.
* A running node advertises itself in predetermined time intervals (default = 30 s).
  * advertise = multicast mode and state.
    * mode = light, button, ...
      * This is the only difference between nodes.
      * Modify ADVERTISE_TO_BACKHAUL_NETWORK_STRING in mesh_led_control_example.cpp to change mode
    * state = on, off, ...


#### Message format:

There are 3 different kinds of messages:
  * (1) Ignore (such as advertise messages to backhaul network)
  * (2) Control (such as light control messages)
    * Receive -> check whether to obey or ignore and act accordingly.
  * (3) Configure (such as setting master_buffer and slave_buffer):
    * Receive -> configure according to the received instructions.
    * UI uses these messages to configure the master_groups and slave_groups.
  
#### Examples

* Advertise: "#advertise:mode;s:%d;", state
  * Example 1: "#advertise:button;s:%d;", state
  * Example 2: "#advertise:light;s:%d;", state
* Light control: "%s;t:lights;s:?;", master_buffer ? master_buffer : "g"
  * Example 1: "group1;t:lights;s:?;"
* Configuration: "conf;slave_buffer;master_buffer"
  * format(slave_buffer) == format(master_buffer) = "group1,grup2,grup3,...,groupN;"
  * Example 1: 
    * (1.1) Confirure node1: "conf;hall,bedroom;hall,upstairs;"
    * (1.2) Confirure node2: "conf;upstairs;;"
    * (1.3) Confirure node3: "conf;mount_everest;moon;"
    * (2) node1 sends light control message to its master_groups "hall" and "upstairs":
    * (3) nodes in the network (including the sender) listen messages to any of their slave_groups:
      * (3.1) node1 belongs to the "hall" group as a slave and thus switches its state
      * (3.2) node2 belongs to the "upstairs" group as a slave and thus switches its state
      * (3.3) node3 belongs to neither "hall" group nor "upstairs" group as a slave and thus does not switch its state

See master/Readme.md for more examples.
