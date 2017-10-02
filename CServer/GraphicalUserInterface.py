
from Tkinter import *

class GraphicalUserInterface:

    def listbox_create(self, root):
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=LEFT, fill=Y)

        listbox = Listbox(root, yscrollcommand=scrollbar.set)
        #for i in range(1000):
        #listbox.insert(END, "First Item")
        #listbox.insert(END, "----------")
        listbox.pack(side=LEFT, fill=BOTH)

        scrollbar.config(command=listbox.yview)

        #listbox.bind('<<ListboxSelect>>', onselect)
        #listbox.bind('<<Button-3>>', onselect)
        
        return (scrollbar, listbox)

    
