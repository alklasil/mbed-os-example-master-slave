/*
* Copyright (c) 2016 ARM Limited. All rights reserved.
* SPDX-License-Identifier: Apache-2.0
* Licensed under the Apache License, Version 2.0 (the License); you may
* not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an AS IS BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#include "mbed.h"
#include "nanostack/socket_api.h"
#include "mesh_led_control_example.h"
#include "common_functions.h"
#include "ip6string.h"
#include "mbed-trace/mbed_trace.h"
#include <ctype.h>

static void init_socket();
static void handle_socket();
static void receive();
static void my_button_isr();
static void send_message();
static void blink();
static void update_state(uint8_t state);
static void handle_message(char* msg, SocketAddress *source_addr);

#define MSG_SIZE 256
// mesh local multicast to all nodes
//#define multicast_addr_str "ff15::abba:abba" // -- only other nodes (lights, buttons, etc), no routers and beyond
#define multicast_addr_str "ff15::ABBA:ABBA"
//#define multicast_addr_str "fd00:db8:ff1:0:c50b:ae81:5858:298f"
//#define multicast_addr_str "ff02::2"
uint8_t multicast_addr[16] = {0};
#define TRACE_GROUP "example"
#define UDP_PORT 1030
#define MESSAGE_WAIT_TIMEOUT (30.0)
#define MASTER_GROUP 0
#define MY_GROUP 1

DigitalOut led_1(MBED_CONF_APP_LED, 1);
InterruptIn my_button(MBED_CONF_APP_BUTTON);
DigitalOut output(D3, 1);
Timeout messageTimeout;

NetworkInterface * network_if;
UDPSocket* my_socket;
// queue for sending messages from button press.
EventQueue queue;
// for LED blinking
Ticker ticker;

uint8_t multi_cast_addr[16] = {0};
uint8_t receive_buffer[MSG_SIZE];
// how many hops the multicast message can go
static const int16_t multicast_hops = 10;
bool button_status = 0;
uint8_t state = 0;

#if MBED_CONF_APP_ENABLE_MASTER_SLAVE_CONTROL_EXAMPLE
void start_advertisingToBackhaulNetwork();
static void advertiseToBackhaulNetwork();
#define ADVERTISE_TO_BACKHAUL_NETWORK_WAIT_TIME (30.0)
Ticker advertiseToBackhaulNetworkTicker;
char master_slave_buffer[MSG_SIZE] = {0};
char * master_buffer = NULL, * slave_buffer = NULL;
// begin advertise with # character, these messages are ignored by normal nodes
#define ADVERTISE_TO_BACKHAUL_NETWORK_STRING "#advertise:button;s:%d", state
// whether to advertise automatically or not
bool advertise;
#endif

void start_mesh_led_control_example(NetworkInterface * interface){
  tr_debug("start_mesh_led_control_example()");
  MBED_ASSERT(MBED_CONF_APP_LED != NC);
  MBED_ASSERT(MBED_CONF_APP_BUTTON != NC);

  network_if = interface;
  stoip6(multicast_addr_str, strlen(multicast_addr_str), multi_cast_addr);
  //stoip6(backhaul_network_addr_str, strlen(backhaul_network_addr_str), backhaul_network_addr);
  init_socket();
}

static void messageTimeoutCallback()
{
  send_message();
}

#if MBED_CONF_APP_ENABLE_MASTER_SLAVE_CONTROL_EXAMPLE
static void advertiseToBackhaulNetwork(){
  if (!advertise) {
    tr_debug("Don't Send advertise to backhaul network");
    return;
  }
  tr_debug("Send advertise to backhaul network");

  char buf[MSG_SIZE];
  int length;

  length = snprintf(buf, sizeof(buf), ADVERTISE_TO_BACKHAUL_NETWORK_STRING);
  MBED_ASSERT(length > 0);
  tr_debug("Sending advertise to backhaul network");
  SocketAddress send_sockAddr(multicast_addr, NSAPI_IPv6, UDP_PORT);
  my_socket->sendto(send_sockAddr, buf, sizeof(buf));
  //After message is sent, it is received from the network
}

void start_advertisingToBackhaulNetwork(){
  advertise = true;
  advertiseToBackhaulNetworkTicker.attach(advertiseToBackhaulNetwork, ADVERTISE_TO_BACKHAUL_NETWORK_WAIT_TIME);
}
#endif

static void blink() {
  led_1 = !led_1;
}

void start_blinking() {
  ticker.attach(blink, 1.0);
}

void cancel_blinking() {
  ticker.detach();
  led_1=1;
}

static void send_message() {
  tr_debug("send msg %d", button_status);

  char buf[MSG_SIZE];
  int length;

  /**
  * Multicast control message is a NUL terminated string of semicolon separated
  * <field identifier>:<value> pairs.
  *
  * Light control message format:
  * t:lights;g:<group_id>;s:<1|0>;\0
  */
#if MBED_CONF_APP_ENABLE_MASTER_SLAVE_CONTROL_EXAMPLE
  length = snprintf(buf, sizeof(buf), "%s;t:lights;s:?;", master_buffer ? master_buffer : "g");
#else
  length = snprintf(buf, sizeof(buf), "t:lights;s:%s;", (button_status ? "1" : "0")) + 1;
#endif
  MBED_ASSERT(length > 0);
  tr_debug("Sending lightcontrol message, %d bytes: %s", length, buf);
  SocketAddress send_sockAddr(multi_cast_addr, NSAPI_IPv6, UDP_PORT);
  my_socket->sendto(send_sockAddr, buf, MSG_SIZE);
  //After message is sent, it is received from the network
}

// As this comes from isr, we cannot use printing or network functions directly from here.
static void my_button_isr() {
  button_status = !button_status;
  queue.call(send_message);
}

static void update_state(uint8_t state) {
  if (state == 1) {
    tr_debug("Turning led on\n");
    led_1 = 0;
    button_status=1;
    output = 0;
  }
  else {
    tr_debug("Turning led off\n");
    led_1 = 1;
    button_status=0;
    output = 1;
  }
}

static void handle_message(char* msg, SocketAddress *source_addr = NULL) {
  // Check if this is lights message

  tr_debug("handle_message: %s", msg);

  if (msg[0] == '#') return;    // for control messages and so on, yes there are better ways to handle this but i aint got the time for implementing such

  // check if the message contains Unprintable char(s)
  char * c = msg;
  while (isprint(*(c++))) ;
  if (*(--c) != '\0') {
    printf("Unprintable char %c at msg[%d]\n", *c, c-msg);
    return;
  }

#if MBED_CONF_APP_ENABLE_MASTER_SLAVE_CONTROL_EXAMPLE
  // msg needs to be null terminated (eg. for strchr)
  if (strncmp(msg, "conf;", strlen("conf;")) == 0) {
    snprintf(master_slave_buffer, sizeof(master_slave_buffer), "%s", (char *)(&msg[strlen("conf;")]));
    tr_debug("set master_slave_buffer: %s", master_slave_buffer);
    // master;slave_groups;master_groups   [groups ~= g1,g2,g3,g4]
    // set slave buffer
    slave_buffer = master_slave_buffer;
    // if the message does not contain slave_buffer, then it cannot contain master_buffer
    if (slave_buffer[0] == '\0') {
      slave_buffer = NULL;
      master_buffer = NULL;
      return;
    }
    // check if message contains master_buffer and whether the buffer contains any items
    master_buffer = strchr(slave_buffer, ';');
    if (master_buffer == NULL) return;
    *master_buffer = '\0';
    master_buffer++;
    if (master_buffer[0] == '\0') master_buffer = NULL;
    return;
  } else if (strncmp(msg, "advertise;", strlen("advertise;")) == 0) {
    if (strstr(msg, "s:1;") != NULL) {
      advertise = 1;
      return;
    } else if (strstr(msg, "s:0;") != NULL) {
      advertise = 0;
      return;
    } else {
      // force advertise
      advertiseToBackhaulNetwork();
      return;
    }
  } else if (strncmp(msg, "send_message;", strlen("send_message;")) == 0) {
    // force send_message (can virtualize light to work as button) [experimental]
    send_message();
    return;
  }

  if (slave_buffer == NULL) return;

  // we belong to at least one slave_group, ie., we may have got masters who to obey to
  char * cmd_slave_buffer = msg;
  char * cmd_slave = cmd_slave_buffer;
  // get command address in the buffer
  char * cmd = strchr(cmd_slave_buffer, ';');
  if (cmd == NULL) return;
  // separate command from the groups
  *cmd = '\0';
  cmd++;
  // if msg contains no command, simply return (for now)
  if (cmd[0] == ';') return;

  bool is_slave = false;
  char * cmd_slave_next = cmd_slave;
  // check if we obey the slave_group to where the sender send the message
  // (ie., the sender sends messages to slave group to which we belong)
  do {
    cmd_slave_next = strchr(cmd_slave, ',');
    if (cmd_slave_next != NULL) cmd_slave_next[0] = '\0';
    if (strstr(slave_buffer, cmd_slave) != NULL) {
      tr_debug( "slave_buffer|cmd_slave: %s|%s\n", slave_buffer, cmd_slave );
      // eg. slave_buffer = "g1,g2", cmd_slave = "g" -> all groups, g1 -> only group g1
      is_slave = true;
      break;
    }
    if (cmd_slave_next != NULL) cmd_slave = cmd_slave_next + 1;
  } while (cmd_slave_next != NULL);

  // if the message was not meant for us, we do not do as it commands
  if (is_slave == false) return;

#else
  // if master_slave example not active, no groups in msg, ie., only command
  char * cmd = msg;
#endif

  // fi (is_slave)
  // .[2K.[33m[WARN][ip6r]: LL addr of fd00:db8:ff1::1 not found.[0m
  if (strstr(cmd, "t:lights;") == NULL) {
    return;
  }

  if (strstr(cmd, "s:?") != NULL) {
    update_state((++state)%2);
  } else if (strstr(cmd, "s:1;") != NULL) {
    update_state(1);
  } else if (strstr(cmd, "s:0;") != NULL) {
    update_state(0);
  }
}

static void receive() {
  // Read data from the socket
  SocketAddress source_addr;
  memset(receive_buffer, 0, sizeof(receive_buffer));
  bool something_in_socket=true;
  // read all messages
  while (something_in_socket) {
    int length = my_socket->recvfrom(&source_addr, receive_buffer, sizeof(receive_buffer) - 1);
    if (length > 0) {
      int timeout_value = MESSAGE_WAIT_TIMEOUT;
      tr_debug("Packet from %s\n", source_addr.get_ip_address());
      //timeout_value += rand() % 30;
      //tr_debug("Advertisiment after %d seconds", timeout_value);
      //messageTimeout.detach();
      //messageTimeout.attach(&messageTimeoutCallback, timeout_value);
      // Handle command - "on", "off"
      handle_message((char*)receive_buffer, &source_addr);
    }
    else if (length!=NSAPI_ERROR_WOULD_BLOCK) {
      tr_error("Error happened when receiving %d\n", length);
      something_in_socket=false;
    }
    else {
      // there was nothing to read.
      something_in_socket=false;
    }
  }
}

static void handle_socket() {
  // call-back might come from ISR
  queue.call(receive);
}

static void init_socket()
{
  my_socket = new UDPSocket(network_if);
  my_socket->set_blocking(false);
  my_socket->bind(UDP_PORT);
  my_socket->setsockopt(SOCKET_IPPROTO_IPV6, SOCKET_IPV6_MULTICAST_HOPS, &multicast_hops, sizeof(multicast_hops));

  ns_ipv6_mreq_t mreq;
  memcpy(mreq.ipv6mr_multiaddr, multi_cast_addr, 16);
  mreq.ipv6mr_interface = 0;

  //void * m = &mreq;
  //my_socket->setsockopt(SOCKET_IPPROTO_IPV6, SOCKET_IPV6_JOIN_GROUP, &mreq, sizeof(mreq));
  //socket_setsockopt((int8_t)my_socket, SOCKET_IPPROTO_IPV6, SOCKET_IPV6_JOIN_GROUP, m, sizeof mreq);

  my_socket->setsockopt(SOCKET_IPPROTO_IPV6, SOCKET_IPV6_JOIN_GROUP, &mreq, sizeof mreq);

  if (MBED_CONF_APP_BUTTON != NC) {
    my_button.fall(&my_button_isr);
    my_button.mode(PullUp);
  }

  //let's register the call-back function.
  //If something happens in socket (packets in or out), the call-back is called.
  my_socket->sigio(callback(handle_socket));
  // dispatch forever
  queue.dispatch();
}
