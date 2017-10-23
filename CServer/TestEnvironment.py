# something like this
# in gui when button pressed invoke run_tests, or possibly one of the sequences

class TestEnvironment:

    def __init__(self):
      pass
      
    def run_tests(self, node):
      # for example when certain button is pressed in the ui (in a node)
      run_sequence(sequence_advertise(node))
      #run_sequence(sequence_test_light(node))
      #run_sequence(sequence_test_button(node))
      #run_sequence(or something..)
      
    def run_sequence(self, sequence):
      # parse
      for item in sequence :
        if item.send:
          # send
          pass
        if imte.receive:
          # receive (should node(in ui) store last received message?)
          if not received == item.receive:
            # error
            pass
          pass
        if item.outcome:
          if not item.outcome():
            # error
            pass
      
    def sequence_advertise(self, node):
      node_test = Node() # empty of gnode and other unnecessary variables (networkinterface node needs modification, for example another init function)
      sequence = TestSequence()
      sequence.add(send="advertise;", receive=FIXME, outcome=lambda: (node_test.test(node)))
      sequence.add(send="advertise;s:1")
      sequence.add(send="advertise;", receive=FIXME, outcome=lambda: (node_test.test(node)))
      sequence.add(send="advertise;s:0")
      sequence.add(send="advertise;", receive=None, wait_time=30, outcome=lambda: (node_test.test(node)))
      sequence.add(receive=FIXME) # normal advertise
      
      return sequence

      

class TestSequence:
    
    def __init__(self):
      pass
      
    def add(self):
      # parse, add to "list"
      pass 
      
    
