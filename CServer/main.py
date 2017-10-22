#!/usr/bin/python
#public
import threading
import time
#private
import MbedNetworkInterface
import GraphicalUserInterface

def main():
    print "main started"
    threads = []
    is_running = True
    graphicalUserInterface = GraphicalUserInterface.GraphicalUserInterface()
    networkInterface = MbedNetworkInterface.MbedNetworkInterface()

    # Collect node related data
    def collect_data():
        time.sleep(2)
        while is_running:
            networkInterface.serve(gnode_parent=graphicalUserInterface.get_root())
        print "collect_data DOWN"

    # Remove outdated data
    def remove_outdated_data():
        time.sleep(2)
        #networkInterface.nodelist.update("::1", "light", graphicalUserInterface.get_root())
        #networkInterface.nodelist.update("2001:0:9d38:6abd:10f4:3b69:ab0f:92a9", "button", graphicalUserInterface.get_root())
        while is_running:
            for i in range(MbedNetworkInterface.OUDATE_TIME):
                if not is_running:
                    break
                time.sleep(1)
            if is_running:
                networkInterface.get_nodelist().removeOutdated()
        print "remove_outdated_data DOWN"

    # Start graphical user interface
    def gui_main():
        graphicalUserInterface.run()
        print "gui_main DOWN"


    # Start threads
    threads.append(threading.Thread(name="gui_main", target=gui_main))
    threads.append(threading.Thread(name="collect_data", target=collect_data))
    threads.append(threading.Thread(name="remove_outdated_data", target=remove_outdated_data))

    for t in threads:
        t.start()

    threads[0].join()

    # Exit
    is_running = False
    # Stop collect-data thread (is waiting for socket to receive a message before checking is_running)
    networkInterface.sendMessage(addr="::1")


if __name__ == '__main__':
    main()
