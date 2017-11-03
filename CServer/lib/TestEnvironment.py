# something like this
# in gui when button pressed invoke run_tests, or possibly one of the sequences

import copy
import time

class TestEnvironment:

    def __init__(self):
      self.test_nodes = []

    def run(self):
        if self.test_nodes:
            test_node = self.test_nodes.pop(0)
            test_node.set_testing(True)
            self.run_tests(test_node)
            test_node.set_testing(False)

    def add_test_node(self, node):
        self.test_nodes.append(node)

    def run_tests(self, node):
      # run tests, for example when certain button is pressed in the ui (in a node)

      # FIXME: add mechanism for stopping the tests, or at least prevent user from using the node when under tests
      node_copy = copy.copy(node)


      def run_tests_all():

          print "running tests <BEGIN>"

          self.run_sequence(node, self.sequence_advertise(node, node_copy))

          print "running tests <END>"

      run_tests_all()

      #node = node_copy

    def run_sequence(self, node, sequence):

      max_wait_time = 30

      def title(v):
          print v

      def set_max_wait_time(v):
          max_wait_time = v

      def send(v):
          node.send(msg=v)

      def receive(v):
          msg, async = v
          timestamp = int(time.time())
          node.set_received(None)
          timeout = True
          time.sleep(1)
          details = []
          while int(time.time()) - timestamp < max_wait_time:
              received = node.get_received()
              if not received is None:
                  if not msg in received:
                      timeout = False
                      details.append(v, " not found in ", received)
                      if not async:
                          return "failure", details
                  else:
                    details.append(v, " found in ", received)
                    return "success", details
              # this is a poor way, use traps or such instead
              time.sleep(1)
          details.append(node)
          return "timeout", details

      def outcome(v):
          if not v():
            return "failure"
          else:
            return "success"

      for item in sequence.get_items():
        for k,v in item:

            if k == 'title':
              title(v)
            elif k == 'max_wait_time':
              max_wait_time = set_max_wait_time(value)
            elif k == 'send':
              send(v)
            elif k == 'receive':
              result, details = receive(value)
              print result
              print details
            elif k == 'outcome':
              result = outcome(v)
              print result
            # TODO:
            #  * better stats keeping (what tests failed, what succeeded, etc)

    def sequence_advertise(self, node, node_copy):

      from collections import OrderedDict

      sequence = TestSequence()
      sequence.add([
        ('title', '<TEST> advertise(1) -- query'),
        ('send', 'advertise;'),
        ('max_wait_time', 300),
        ('receive', ('#advertise:' + node.get_node_mode() + ';', True)),
        ('outcome', lambda: 1 == 1) # FIXME change to something that makes sense
      ])
      sequence.add([
        ('title', '<TEST> advertise(1) -- set'),
        ('send', 'advertise;s:1')
      ])
      #sequence.add(node=node, send="advertise;", receive=FIXME, outcome=lambda: (node_test.test(node)))
      #sequence.add(node=node, send="advertise;s:0")
      #sequence.add(node=node, send="advertise;", receive=None, wait_time=30, outcome=lambda: (node_test.test(node)))
      #sequence.add(node=node, receive=FIXME) # normal advertise

      return sequence



class TestSequence:

    def __init__(self):
      self.items = []

    def add(self, item):
      self.items.append(item)

    def get_items(self):
        return self.items
