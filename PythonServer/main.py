#!/usr/bin/python
#public
import threading
import time
#private
from lib.MbedNetworkInterface import MbedNetworkInterface
from lib.GraphicalUserInterface import GraphicalUserInterface

from kivy.core.clipboard import Clipboard

def main():
    threads = []
    is_running = True
    graphicalUserInterface = GraphicalUserInterface()
    networkInterface = MbedNetworkInterface()

    # collect node related data
    def collect_data():
        print("collect_data thread UP")
        # wait for 2 seconds to make sure gui is up
        time.sleep(2)
        while is_running:
            networkInterface.serve(gnode_parent=graphicalUserInterface.get_root())
        print("collect_data thread DOWN")

    # remove outdated data
    def remove_outdated_data():
        print("remove_outdated_data thread UP")
        # wait for 2 seconds to make sure gui is up
        time.sleep(2)
        # DummyNode, remove comments if you want to show this
        #networkInterface.nodelist.update(
        #    "Most recently received message is shown here",
        #    "Ip slot (IPV6 supported)",
        #    "DummyNode",
        #    graphicalUserInterface.get_root(),
        #    "See readme.md for instructions on message format"
        #)

        networkInterface.get_nodelist().update_from_text(
            node = None,
            text = Clipboard.paste(),
            selected_nodes = "all",
            gnode_parent=graphicalUserInterface.get_root()
        )


        while is_running:
            for i in range(networkInterface.get_outdate_time()):
                if not is_running:
                    break
                time.sleep(1)
            if is_running:
                networkInterface.get_nodelist().removeOutdated()
        print("remove_outdated_data thread DOWN")

    def gui_main():
        print("gui_main thread UP")
        graphicalUserInterface.run()
        print("gui_main thread DOWN")


    # create threads
    threads.append(threading.Thread(name="gui_main", target=gui_main))
    threads.append(threading.Thread(name="collect_data", target=collect_data))
    threads.append(threading.Thread(name="remove_outdated_data", target=remove_outdated_data))

    # Start threads
    for t in threads:
        t.start()

    # join the gui_main-thread
    threads[0].join()

    # when exiting the gui_main-thread, tell all threads to stop
    is_running = False
    # send networkInterface a message so that it knows to stop the recv-function
    networkInterface.sendMessage(addr="::1")


if __name__ == '__main__':
    # start main-function
    main()
