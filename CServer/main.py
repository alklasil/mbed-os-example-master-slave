#!/usr/bin/python
from Tkinter import *
import threading
import MbedNetworkInterface
import GraphicalUserInterface

def main():

    print "main started"
    threads = []
    is_running = True
    graphicalUserInterface = GraphicalUserInterface.GraphicalUserInterface()
    root = Tk()

    networkInterface = MbedNetworkInterface.MbedNetworkInterface()
    
    # collect node related data
    def collect_data():
        while is_running:
            networkInterface.serve()
    threads.append(threading.Thread(name="collect_data", target=collect_data))
    
    # remove outdated data

    def remove_outdated_data():
        import time
        while is_running:
            time.sleep(MbedNetworkInterface.OUDATE_TIME)
            print "do remove_outdated_data"
            networkInterface.get_nodelist().removeOutdated()
    threads.append(threading.Thread(name="remove_outdated_data", target=remove_outdated_data))

    # Tkinker
    def onselect(evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'You selected item %d: "%s"' % (index, value)

    def listbox_update(listbox, mode=None):
        #if mode is None:
        #    nodes = networkInterface.get_nodes()
        #else:
        #    nodes = networkInterface.get_nodes_by_mode(mode)

        nodes = []
        nodes.append(MbedNetworkInterface.Node("222", "111:111:111:11", "light"))
        nodes.append(MbedNetworkInterface.Node("222", "111:111:111:12", "light"))
        nodes.append(MbedNetworkInterface.Node("222", "111:111:111:13", "light"))
        nodes.append(MbedNetworkInterface.Node("222", "111:111:111:14", "light"))

        listbox.delete(0,END)

        for node in nodes:
            listbox.insert(END, node.get_node_mode() + " - " + node.get_addr())
        listbox.pack(side=LEFT, fill=BOTH)
    
    def tkinker_main():

        #button_nodes = networkInterface.get_nodelist().get_nodes_by_mode("button")
        #light_nodes = networkInterface.get_nodelist().get_nodes_by_mode("light")

        root.geometry('{}x{}'.format(640, 480))

        #T = Text(root, height=2, width=30)
        #T.pack()
        #T.insert(END, "Just a text Widget\nin two lines\n")

        #nodes_all = graphicalUserInterface.listbox_create(root)
        #nodes_slave = graphicalUserInterface.listbox_create(root)
        #nodes_master = graphicalUserInterface.listbox_create(root)

        #listbox_update(nodes_all[1])

        root.mainloop()
    threads.append(threading.Thread(name="tkinker_main", target=tkinker_main))

    # Start threads
    for t in threads:
        t.start()
    threads[-1].join()

    # exit
    is_running = False
    networkInterface.sendMessage()


if __name__ == '__main__':
    main()
