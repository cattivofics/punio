from tkinter import Label, Entry
import tkSimpleDialog


class LayoutDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        Label(master, text="Enter the name of the layout:").grid(row=0)
        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1

    def apply(self):
        self.result = self.e1.get()