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
          # run_sequence(sequence_test_light(node))
          # run_sequence(sequence_test_button(node))
          # run_sequence(or something..)

          print "running tests <END>"

      run_tests_all()

      #node = node_copy

    def run_sequence(self, node, sequence):

      # parseter
      for item in sequence.get_items():
        for i in item:
            k = i[0]
            v = i[1]
            print "......"
            print k, v
            print "------"

            if k == 'title':
              print v
            if k == 'max_wait_time':
              max_wait_time = v
            elif k == 'send':
              node.send(msg=v)
            elif k == 'receive':
              print "sdfasdfsadREC"
              # receive (should node(in ui) store last received message?)
              timestamp = int(time.time())
              node.set_received(None)
              timeout = True
              time.sleep(1)
              while int(time.time()) - timestamp < max_wait_time:
                  # consider for example traps of some sort (when received changes) instead of a whileloop
                  received = node.get_received()
                  if not received is None:
                      if not v in received:
                          # FIXME
                          print '(received != item.receive)'
                          print item
                          timeout = False
                          break
                      else:
                        # SUCCESS
                        print "suzess"
                        break
                  time.sleep(1)
              if timeout == True:
                  print "timeout"
            elif k == 'outcome':
              if not v():
                # FIXME
                print "item.outcome() failure"
                print item
              else:
                # SUCCESS
                pass

    def sequence_advertise(self, node, node_copy):

      from collections import OrderedDict

      sequence = TestSequence()
      sequence.add([
        ('title', '<TEST> advertise(1) -- query'),
        ('send', 'advertise;'),
        ('max_wait_time', 30),
        ('receive', '#advertise:' + node.get_node_mode() + ';'),
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
